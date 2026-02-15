"""Results tools: list campaigns, get results, extract PoCs, generate JSON reports."""

import asyncio
import csv
import json
import os
import re
import sys
import tarfile

from mcp.server.fastmcp import FastMCP

from ..core import paths
from ..core.task_manager import TaskType, task_manager


def register(mcp: FastMCP):
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

    async def _parse_campaign_results(
        workdir: str,
        fuzzer: str,
        target: str,
        program: str,
        run_id: str,
    ) -> dict:
        async def _start_poc_extraction(shared_dir: str) -> dict:
            from ..core.config_parser import parse_configrc

            if not os.path.isdir(shared_dir):
                return {"error": f"Shared directory not found: {shared_dir}"}

            poc_dir = os.path.join(workdir, "poc")
            os.makedirs(poc_dir, exist_ok=True)
            before = set(os.listdir(poc_dir))

            try:
                config = parse_configrc(target)
            except Exception as e:
                return {"error": f"Failed to parse configrc: {e}"}

            args = config["program_args"].get(program, "")

            env = {
                "FUZZER": fuzzer,
                "TARGET": target,
                "PROGRAM": program,
                "ARGS": args,
                "SHARED": shared_dir,
                "POCDIR": poc_dir,
                "MAGMA": str(paths.MAGMA_ROOT),
            }

            merged_env = {**os.environ, **env}
            process = await asyncio.create_subprocess_exec(
                "bash",
                str(paths.EXTRACT_SH),
                env=merged_env,
                cwd=str(paths.MAGMA_ROOT),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            output, _ = await process.communicate()

            result = {
                "poc_dir": poc_dir,
                "status": "completed" if process.returncode == 0 else "failed",
                "exit_code": process.returncode,
            }
            after = set(os.listdir(poc_dir))
            prefix = f"{fuzzer}_{target}_{program}_"
            created = sorted(after - before)
            result["pocs"] = [
                os.path.join(poc_dir, name)
                for name in created
                if name.startswith(prefix)
            ]
            if process.returncode != 0:
                text = output.decode("utf-8", errors="replace").strip()
                if text:
                    result["error"] = text.splitlines()[-1]
            return result

        def _map_pocs_to_bugs(
            bugs: list[dict],
            poc_paths: list[str],
        ) -> tuple[list[dict], list[str]]:
            bug_to_pocs = {b["id"]: [] for b in bugs}
            new_or_unknown: list[str] = []
            prefix = f"{fuzzer}_{target}_{program}_"

            for poc_path in poc_paths:
                name = os.path.basename(poc_path)
                if not name.startswith(prefix):
                    continue
                suffix = name[len(prefix):]
                bug_key = suffix.split(".", 1)[0]
                if bug_key == "NEW":
                    new_or_unknown.append(poc_path)
                    continue
                if bug_key in bug_to_pocs:
                    bug_to_pocs[bug_key].append(poc_path)
                else:
                    new_or_unknown.append(poc_path)

            for bug in bugs:
                bug["pocs"] = bug_to_pocs.get(bug["id"], [])
            return bugs, new_or_unknown

        campaign_path = os.path.join(workdir, "ar", fuzzer, target, program, run_id)
        if not os.path.isdir(campaign_path):
            return {
                "error": f"Campaign directory not found in archive: {campaign_path}"
            }

        import shutil
        import tempfile

        tmpdir = None
        try:
            monitor_dir = os.path.join(campaign_path, "monitor")
            if os.path.isdir(monitor_dir):
                rows = _read_monitor_rows(monitor_dir)
            else:
                tarball = os.path.join(campaign_path, "ball.tar")
                if not os.path.isfile(tarball):
                    tarball = os.path.join(campaign_path, "findings.tar")
                if not os.path.isfile(tarball):
                    return {
                        "error": "No monitor directory or tarball found for this campaign."
                    }
                tmpdir = tempfile.mkdtemp(prefix="magma_results_")
                extracted_monitor = os.path.join(tmpdir, "monitor")
                os.makedirs(extracted_monitor, exist_ok=True)
                extracted_count = _extract_monitor_from_tarball(tarball, extracted_monitor)
                if extracted_count == 0:
                    return {"error": f"No monitor snapshots found in tarball: {tarball}"}
                rows = _read_monitor_rows(extracted_monitor)

            if not rows:
                return {
                    "fuzzer": fuzzer,
                    "target": target,
                    "program": program,
                    "run_id": run_id,
                    "bugs": [],
                    "note": "No monitor data available.",
                }

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

            result = {
                "fuzzer": fuzzer,
                "target": target,
                "program": program,
                "run_id": run_id,
                "bugs": bugs
            }
            result["poc_extraction"] = await _start_poc_extraction(campaign_path)
            poc_paths = result["poc_extraction"].get("pocs", [])
            mapped_bugs, new_or_unknown = _map_pocs_to_bugs(bugs, poc_paths)
            result["bugs"] = mapped_bugs
            result["new_or_unknown_pocs"] = new_or_unknown
            return result
        except Exception as e:
            return {"error": f"Failed to parse campaign results: {e}"}
        finally:
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)

    @mcp.tool()
    async def magma_get_campaign_results(
        batch_id: str,
        task_ids: list[str] | None = None,
    ) -> str:
        """Get per-bug reach/trigger timing data for campaign tasks in a batch.

        Parses monitor snapshots directly from campaign output and reports
        first reach/trigger timestamps per bug. Also extracts PoCs for each
        campaign run.

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

        results = []
        for tid in targets:
            record = task_manager.get(tid)
            if record is None:
                results.append({"task_id": tid, "error": "Task not found"})
                continue
            if record.task_type != TaskType.CAMPAIGN:
                results.append({
                    "task_id": tid,
                    "status": record.status.value,
                    "error": f"Task type is '{record.task_type.value}', expected 'campaign'",
                })
                continue
            if record.status.value == "queued":
                results.append({
                    "task_id": tid,
                    "status": record.status.value,
                    "error": "Task has not started yet; no campaign results available.",
                })
                continue

            match = re.fullmatch(r"campaign ([^/]+)/([^/]+)/([^/]+)/([^/]+)", record.description)
            if not match:
                results.append({
                    "task_id": tid,
                    "status": record.status.value,
                    "error": f"Could not parse campaign coordinates from description: {record.description}",
                })
                continue

            fuzzer, target, program, run_id = match.groups()
            parsed = await _parse_campaign_results(
                workdir=workdir,
                fuzzer=fuzzer,
                target=target,
                program=program,
                run_id=run_id,
            )
            parsed["task_id"] = tid
            parsed["status"] = record.status.value

            results.append(parsed)

        return json.dumps({
            "batch_id": batch_id,
            "results": results,
        }, indent=2)
