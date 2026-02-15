"""Results tools: list campaigns, get results, extract PoCs, generate JSON reports."""

import asyncio
import csv
import json
import os
import re
import shutil
import tarfile
import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from ..core import paths
from ..core.task_manager import TaskRecord, TaskStatus, TaskType, task_manager


# File lock for atomic read-modify-write of results.json
_results_lock = asyncio.Lock()

# Track which campaign task_ids already have extraction tasks spawned
_extract_tasks: dict[str, str] = {}  # campaign_task_id -> extract_task_id


def _extract_monitor_from_tarball(tarball: str, monitor_dir: str) -> int:
    """Extract monitor snapshots from a campaign tarball into monitor_dir."""
    extracted = 0
    with tarfile.open(tarball, "r") as tf:
        for member in tf.getmembers():
            if not member.isfile():
                continue

            parts = [p for p in member.name.split("/") if p and p != "."]
            if "monitor" not in parts:
                continue

            idx = parts.index("monitor")
            rel_parts = parts[idx + 1:]
            if not rel_parts:
                continue

            dst_path = os.path.join(monitor_dir, *rel_parts)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                continue
            with src, open(dst_path, "wb") as out:
                out.write(src.read())
            extracted += 1
    return extracted


def _read_monitor_rows(monitor_dir: str) -> list[tuple[int, dict[str, str]]]:
    """Read monitor CSV snapshots as (timestamp_s, row_dict)."""
    rows: list[tuple[int, dict[str, str]]] = []
    files = [f for f in os.listdir(monitor_dir) if f.isdigit()]
    files.sort(key=int)

    for fname in files:
        path = os.path.join(monitor_dir, fname)
        try:
            with open(path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                row = next(reader, None)
                if row is None:
                    continue
                rows.append((int(fname), row))
        except OSError:
            continue
    return rows


def _parse_monitor_bugs(
    monitor_dir: str,
) -> list[dict] | None:
    """Parse monitor data into bug reach/trigger timing. Returns None if no data."""
    rows = _read_monitor_rows(monitor_dir)
    if not rows:
        return None

    reached: dict[str, int] = {}
    triggered: dict[str, int] = {}
    bug_ids: set[str] = set()

    for timestamp, row in rows:
        for key, raw_value in row.items():
            if not key or len(key) < 3:
                continue
            if not (key.endswith("_R") or key.endswith("_T")):
                continue
            bug_id = key[:-2]
            bug_ids.add(bug_id)
            try:
                value = int(raw_value)
            except (TypeError, ValueError):
                value = 0
            if value <= 0:
                continue
            if key.endswith("_R") and bug_id not in reached:
                reached[bug_id] = timestamp
            elif key.endswith("_T") and bug_id not in triggered:
                triggered[bug_id] = timestamp

    bugs = []
    for bug in sorted(bug_ids):
        bugs.append({
            "id": bug,
            "reached": bug in reached,
            "triggered": bug in triggered,
            "time_to_first_reached_s": reached.get(bug),
            "time_to_first_triggered_s": triggered.get(bug),
        })
    return bugs


def _get_monitor_dir(campaign_path: str) -> tuple[str, str | None]:
    """Resolve the monitor dir for a campaign, extracting from tarball if needed.

    Returns (monitor_dir, tmpdir_to_cleanup_or_None).
    Raises FileNotFoundError if no monitor data is available.
    """
    monitor_dir = os.path.join(campaign_path, "monitor")
    if os.path.isdir(monitor_dir):
        return monitor_dir, None

    tarball = os.path.join(campaign_path, "ball.tar")
    if not os.path.isfile(tarball):
        tarball = os.path.join(campaign_path, "findings.tar")
    if not os.path.isfile(tarball):
        raise FileNotFoundError(
            "No monitor directory or tarball found for this campaign."
        )

    tmpdir = tempfile.mkdtemp(prefix="magma_results_")
    extracted_monitor = os.path.join(tmpdir, "monitor")
    os.makedirs(extracted_monitor, exist_ok=True)
    extracted_count = _extract_monitor_from_tarball(tarball, extracted_monitor)
    if extracted_count == 0:
        shutil.rmtree(tmpdir, ignore_errors=True)
        raise FileNotFoundError(
            f"No monitor snapshots found in tarball: {tarball}"
        )
    return extracted_monitor, tmpdir


def _map_cases_to_bugs(
    bugs: list[dict],
    case_lines: list[dict],
) -> list[dict]:
    bug_to_cases = {b["id"]: [] for b in bugs}

    for case in case_lines:
        bug_key = case["bug_id"]
        if bug_key in bug_to_cases:
            bug_to_cases[bug_key].append(case)

    for bug in bugs:
        cases = bug_to_cases.get(bug["id"], [])
        bug["cases"] = cases
        bug["testcases_that_reached"] = [
            c["file"] for c in cases if c.get("reached", 0) > 0
        ]
        bug["testcases_that_triggered"] = [
            c["file"] for c in cases if c.get("triggered", 0) > 0
        ]
    return bugs


def _parse_extract_output(text: str) -> dict:
    """Parse the stdout of extract2.sh into structured testcase analysis.

    extract2.sh outputs lines in the format:
        <filepath> exit_code <N> bug <BUGID>
    where exit_code comes from magma/runonce.sh and BUGID is the triggered bug.
    """
    result: dict = {
        "status": "completed",
        "lines": [],
        "unparsed_lines": [],
    }

    # Format: <filepath> exit_code <N> bug <BUGID>
    line_re = re.compile(
        r"^(?P<file>\S+)\s+"
        r"exit_code\s+(?P<exit_code>\d+)\s+"
        r"bug\s+(?P<bug_id>\S+)\s*$"
    )
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = line_re.match(stripped)
        if not match:
            result["unparsed_lines"].append(stripped)
            continue
        result["lines"].append({
            "file": match.group("file"),
            "bug_id": match.group("bug_id"),
            "exit_code": int(match.group("exit_code")),
            "triggered": 1,
            "reached": 1,
        })
    return result


async def _save_result_to_disk(workdir: str, batch_id: str, entry: dict) -> None:
    """Atomically merge a single campaign result entry into {workdir}/results.json."""
    results_path = os.path.join(workdir, "results.json")

    async with _results_lock:
        existing: dict = {"batch_id": batch_id, "results": []}
        if os.path.isfile(results_path):
            try:
                with open(results_path) as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        # Update or append by task_id
        results_list = existing.get("results", [])
        updated = False
        for i, r in enumerate(results_list):
            if r.get("task_id") == entry.get("task_id"):
                results_list[i] = entry
                updated = True
                break
        if not updated:
            results_list.append(entry)

        existing["results"] = results_list

        # Atomic write
        fd, tmp = tempfile.mkstemp(
            dir=workdir, suffix=".tmp", prefix="results_"
        )
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(existing, f, indent=2)
            os.replace(tmp, results_path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise


def register(mcp: FastMCP):

    async def _spawn_extraction(
        workdir: str,
        batch_id: str,
        campaign_task_id: str,
        fuzzer: str,
        target: str,
        program: str,
        run_id: str,
    ) -> TaskRecord:
        """Spawn an async extraction task for a single campaign run."""
        from ..core.config_parser import parse_configrc

        campaign_path = os.path.join(workdir, "ar", fuzzer, target, program, run_id)

        try:
            config = parse_configrc(target)
        except Exception:
            config = {"program_args": {}}

        args = config["program_args"].get(program, "")
        log_dir = os.path.join(workdir, "log")
        os.makedirs(log_dir, exist_ok=True)
        log_file = Path(log_dir) / f"extract_{fuzzer}_{target}_{program}_{run_id}.log"

        env = {
            "FUZZER": fuzzer,
            "TARGET": target,
            "PROGRAM": program,
            "ARGS": args,
            "SHARED": campaign_path,
            "MAGMA": str(paths.MAGMA_ROOT),
        }

        description = f"extract {fuzzer}/{target}/{program}/{run_id}"

        async def _on_finish(record: TaskRecord) -> None:
            """Parse extraction output + monitor data, save to results.json."""
            # Read the extraction log
            text = ""
            if record.log_file and os.path.isfile(record.log_file):
                try:
                    with open(record.log_file) as f:
                        text = f.read()
                except OSError:
                    pass

            testcase_analysis = _parse_extract_output(text)
            if record.exit_code != 0:
                testcase_analysis["status"] = "failed"
                testcase_analysis["exit_code"] = record.exit_code
                last_line = text.strip().splitlines()[-1] if text.strip() else ""
                testcase_analysis["error"] = last_line

            # Parse monitor data
            tmpdir = None
            try:
                monitor_path, tmpdir = _get_monitor_dir(campaign_path)
                bugs = _parse_monitor_bugs(monitor_path) or []
            except FileNotFoundError:
                bugs = []
            finally:
                if tmpdir:
                    shutil.rmtree(tmpdir, ignore_errors=True)

            case_lines = testcase_analysis.get("lines", [])
            bugs = _map_cases_to_bugs(bugs, case_lines)

            entry = {
                "task_id": campaign_task_id,
                "extract_task_id": record.task_id,
                "fuzzer": fuzzer,
                "target": target,
                "program": program,
                "run_id": run_id,
                "status": record.status.value,
                "bugs": bugs,
                "testcase_analysis": testcase_analysis,
            }

            await _save_result_to_disk(workdir, batch_id, entry)

        record = await task_manager.spawn(
            task_type=TaskType.EXTRACT,
            description=description,
            cmd=["bash", str(paths.EXTRACT2_SH)],
            env=env,
            cwd=str(paths.MAGMA_ROOT),
            on_finish=_on_finish,
            metadata={
                "batch_id": batch_id,
                "campaign_task_id": campaign_task_id,
            },
            log_file=log_file,
        )

        _extract_tasks[campaign_task_id] = record.task_id
        return record

    @mcp.tool()
    async def magma_get_campaign_results(
        batch_id: str,
        task_ids: list[str] | None = None,
    ) -> str:
        """Get per-bug reach/trigger timing data for campaign tasks in a batch.

        Spawns async extraction tasks (TaskType.EXTRACT) for each campaign run.
        Results are saved to {workdir}/results.json when extraction completes.
        Returns immediately with extract task IDs for tracking, plus any cached
        results already on disk.

        Args:
            batch_id: The batch_id returned by magma_start_campaign.
            task_ids: Optional list of specific task IDs to parse. If empty/null, parses all tasks in the batch.
        """
        from .campaign import _batches

        if batch_id not in _batches:
            return json.dumps({"error": f"Batch not found: {batch_id}"})

        batch = _batches[batch_id]
        workdir = batch["workdir"]
        targets = task_ids if task_ids else batch["task_ids"]

        extract_info = []
        for tid in targets:
            record = task_manager.get(tid)
            if record is None:
                extract_info.append({"task_id": tid, "error": "Task not found"})
                continue
            if record.task_type != TaskType.CAMPAIGN:
                continue
            if record.status.value == "queued":
                extract_info.append({
                    "task_id": tid,
                    "status": record.status.value,
                    "error": "Task has not started yet; no campaign results available.",
                })
                continue

            match = re.fullmatch(
                r"campaign ([^/]+)/([^/]+)/([^/]+)/([^/]+)", record.description
            )
            if not match:
                extract_info.append({
                    "task_id": tid,
                    "status": record.status.value,
                    "error": f"Could not parse campaign coordinates from description: {record.description}",
                })
                continue

            fuzzer, target, program, run_id = match.groups()

            # Check if extraction already spawned for this campaign
            if tid in _extract_tasks:
                ext_id = _extract_tasks[tid]
                ext_record = task_manager.get(ext_id)
                extract_info.append({
                    "task_id": tid,
                    "extract_task_id": ext_id,
                    "status": ext_record.status.value if ext_record else "unknown",
                })
                continue

            # Check if campaign archive dir exists
            campaign_path = os.path.join(
                workdir, "ar", fuzzer, target, program, run_id
            )
            if not os.path.isdir(campaign_path):
                extract_info.append({
                    "task_id": tid,
                    "status": record.status.value,
                    "error": f"Campaign directory not found in archive: {campaign_path}",
                })
                continue

            # Spawn extraction task
            ext_record = await _spawn_extraction(
                workdir=workdir,
                batch_id=batch_id,
                campaign_task_id=tid,
                fuzzer=fuzzer,
                target=target,
                program=program,
                run_id=run_id,
            )
            extract_info.append({
                "task_id": tid,
                "extract_task_id": ext_record.task_id,
                "status": ext_record.status.value,
            })

        # Load cached results from disk if available
        results_path = os.path.join(workdir, "results.json")
        cached_results = None
        if os.path.isfile(results_path):
            try:
                with open(results_path) as f:
                    cached_results = json.load(f).get("results", [])
            except (json.JSONDecodeError, OSError):
                pass

        response: dict = {
            "batch_id": batch_id,
            "extract_tasks": extract_info,
        }
        if cached_results is not None:
            response["results"] = cached_results

        return json.dumps(response, indent=2)

    @mcp.tool()
    async def magma_run_testcase(
        batch_id: str,
        task_id: str,
        filepath: str,
    ) -> str:
        """Run a single test case against a campaign's target and check which bugs it triggers.

        Spins up a Docker container for the campaign's fuzzer/target image,
        runs the test case through the Magma monitor, and reports reach/trigger
        status for each bug.

        Args:
            batch_id: The batch_id from magma_start_campaign.
            task_id: A campaign task_id from the batch (used to resolve fuzzer/target/program).
            filepath: Absolute path to the test case file on the host.
        """
        from .campaign import _batches
        from ..core.config_parser import parse_configrc

        if batch_id not in _batches:
            return json.dumps({"error": f"Batch not found: {batch_id}"})

        record = task_manager.get(task_id)
        if record is None:
            return json.dumps({"error": f"Task not found: {task_id}"})
        if record.task_type != TaskType.CAMPAIGN:
            return json.dumps({
                "error": f"Task type is '{record.task_type.value}', expected 'campaign'"
            })

        match = re.fullmatch(
            r"campaign ([^/]+)/([^/]+)/([^/]+)/([^/]+)", record.description
        )
        if not match:
            return json.dumps({
                "error": f"Could not parse campaign coordinates from description: {record.description}"
            })

        fuzzer, target, program, run_id = match.groups()

        if not os.path.isfile(filepath):
            return json.dumps({"error": f"File not found: {filepath}"})

        try:
            config = parse_configrc(target)
        except Exception:
            config = {"program_args": {}}
        program_args = config["program_args"].get(program, "")

        env = {
            "FUZZER": fuzzer,
            "TARGET": target,
            "PROGRAM": program,
            "ARGS": program_args,
        }
        merged_env = {**os.environ, **env}

        process = await asyncio.create_subprocess_exec(
            "bash", str(paths.CAPTAIN_RUNONCE_SH), filepath,
            env=merged_env,
            cwd=str(paths.MAGMA_ROOT),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        output, _ = await process.communicate()
        text = output.decode("utf-8", errors="replace").strip()

        result: dict = {
            "batch_id": batch_id,
            "task_id": task_id,
            "filepath": filepath,
            "fuzzer": fuzzer,
            "target": target,
            "program": program,
            "exit_code": process.returncode,
            "bug_triggered": None,
            "raw_output": text,
        }

        # Parse "exit_code N bug BUGID" from output
        bug_match = re.search(r"bug\s+(\S+)", text)
        if bug_match:
            result["bug_triggered"] = bug_match.group(1)

        return json.dumps(result, indent=2)
