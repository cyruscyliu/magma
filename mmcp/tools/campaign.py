"""Campaign tools: start/stop fuzzing campaigns, check task status."""

import asyncio
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from ..core import docker_utils, paths
from ..core.cpu_allocator import cpu_allocator
from ..core.task_manager import TaskStatus, TaskType, task_manager

# Base directory for all batch workdirs
_BATCHES_DIR = paths.MAGMA_ROOT / "workdirs"

# In-memory batch registry: batch_id -> {workdir, task_ids}
_batches: dict[int, dict] = {}


def _next_batch_id() -> int:
    """Return the next available batch ID, considering both disk and memory."""
    _BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    existing = set()
    for d in os.listdir(_BATCHES_DIR):
        if d.isdigit():
            existing.add(int(d))
    existing.update(_batches.keys())
    return max(existing, default=-1) + 1


def _get_workdir(batch_id: int) -> str:
    """Get or create the workdir for a batch ID."""
    if batch_id in _batches:
        return _batches[batch_id]["workdir"]
    workdir = str(_BATCHES_DIR / str(batch_id))
    for sub in ("ar", "cache", "log", "poc"):
        os.makedirs(os.path.join(workdir, sub), exist_ok=True)
    _batches[batch_id] = {"workdir": workdir, "task_ids": []}
    return workdir


def _archive_cache(cache_dir: str, ar_dir: str, no_archive: bool) -> None:
    """Move or tar cache results into the archive directory.

    Args:
        cache_dir: Source dir under cache/ (e.g. cache/fuzzer/target/program/run_id/)
        ar_dir: Destination dir under ar/ (e.g. ar/fuzzer/target/program/run_id/)
        no_archive: If True, move directly. If False, tar then delete cache.
    """
    if not os.path.isdir(cache_dir):
        return
    os.makedirs(ar_dir, exist_ok=True)
    if no_archive:
        # Move cache contents directly into ar dir
        for item in os.listdir(cache_dir):
            src = os.path.join(cache_dir, item)
            dst = os.path.join(ar_dir, item)
            shutil.move(src, dst)
        shutil.rmtree(cache_dir, ignore_errors=True)
    else:
        tar_path = os.path.join(ar_dir, "findings.tar")
        subprocess.run(
            ["tar", "-cf", tar_path, "-C", cache_dir, "."],
            check=True, capture_output=True,
        )
        shutil.rmtree(cache_dir, ignore_errors=True)


def _next_run_id(ar_base: str) -> int:
    """Return the next available integer run ID under ar_base."""
    os.makedirs(ar_base, exist_ok=True)
    existing = {int(d) for d in os.listdir(ar_base) if d.isdigit()}
    return max(existing, default=-1) + 1


def register(mcp: FastMCP):

    async def _launch_one(
        fuzzer: str,
        target: str,
        program: str,
        args: str,
        timeout: str,
        poll: int,
        num_cpus: int,
        fuzz_args: str,
        workdir: str,
        run_id: int,
        no_archive: bool = False,
    ) -> dict:
        """Launch a single campaign instance.

        Directory layout:
            workdir/cache/{fuzzer}/{target}/{program}/{run_id}/  — SHARED during run
            workdir/ar/{fuzzer}/{target}/{program}/{run_id}/     — archived after run
            workdir/log/{fuzzer}_{target}_{program}_{run_id}_container.log
        """
        cache_dir = os.path.join(workdir, "cache", fuzzer, target, program, str(run_id))
        ar_dir = os.path.join(workdir, "ar", fuzzer, target, program, str(run_id))
        os.makedirs(cache_dir, exist_ok=True)

        description = f"campaign {fuzzer}/{target}/{program}/{run_id}"

        env = {
            "FUZZER": fuzzer,
            "TARGET": target,
            "PROGRAM": program,
            "ARGS": args,
            "FUZZARGS": fuzz_args,
            "POLL": str(poll),
            "TIMEOUT": timeout,
            "SHARED": cache_dir,
            "MAGMA": str(paths.MAGMA_ROOT),
        }
        cmd = ["bash", str(paths.START_SH)]
        cwd = str(paths.MAGMA_ROOT)

        result_base = {"run_id": run_id, "ar_dir": ar_dir}

        # Build the on_finish callback: archive + optional CPU release
        async def _on_finish(record):
            _archive_cache(cache_dir, ar_dir, no_archive)
            if num_cpus > 0:
                await cpu_allocator.release(record.task_id)

        # Auto-allocate num_cpus
        if num_cpus > 0:
            if num_cpus > cpu_allocator.pool_size:
                return {
                    **result_base,
                    "error": f"Requested {num_cpus} CPUs but pool only has {cpu_allocator.pool_size}",
                }

            allocated = await cpu_allocator.allocate(num_cpus, "_pending")
            if allocated is not None:
                affinity_str = ",".join(str(c) for c in allocated)
                env["AFFINITY"] = affinity_str

                record = await task_manager.spawn(
                    task_type=TaskType.CAMPAIGN,
                    description=description,
                    cmd=cmd, env=env, cwd=cwd,
                    on_finish=_on_finish,
                )
                async with cpu_allocator._lock:
                    cpus = cpu_allocator._allocated.pop("_pending", set())
                    if cpus:
                        cpu_allocator._allocated[record.task_id] = cpus

                return {
                    **result_base,
                    "task_id": record.task_id,
                    "affinity": affinity_str,
                    "status": "started",
                }
            else:
                queued_record = task_manager.register_queued(
                    task_type=TaskType.CAMPAIGN,
                    description=description,
                    on_finish=_on_finish,
                )
                req = await cpu_allocator.enqueue(num_cpus, queued_record.task_id)

                run_env = dict(env)

                async def _wait_and_start():
                    await req.event.wait()
                    if req.cancelled:
                        return
                    aff = ",".join(str(c) for c in req.allocated_cpus)
                    run_env["AFFINITY"] = aff
                    await task_manager.start_queued(
                        queued_record, cmd=cmd, env=run_env, cwd=cwd,
                    )

                asyncio.create_task(_wait_and_start())

                return {
                    **result_base,
                    "task_id": queued_record.task_id,
                    "num_cpus_requested": num_cpus,
                    "status": "queued",
                }

        # No affinity requested
        record = await task_manager.spawn(
            task_type=TaskType.CAMPAIGN,
            description=description,
            cmd=cmd, env=env, cwd=cwd,
            on_finish=_on_finish,
        )

        return {
            **result_base,
            "task_id": record.task_id,
            "status": "started",
        }

    @mcp.tool()
    async def magma_start_campaign(
        fuzzer: str,
        target: str,
        program: str,
        args: str = "",
        fuzz_args: str = "",
        timeout: str = "1m",
        repeat: int = 1,
        num_cpus: int = 0,
        poll: int = 5,
        no_archive: bool = False,
    ) -> str:
        """Start fuzzing campaign(s) in Docker containers. Returns task_id(s) for tracking.

        The Docker image must already be built via magma_build_image.

        During the campaign, findings are written to cache/. When the campaign
        finishes, results are archived into ar/ (tar by default, or moved
        directly if no_archive is set).

        Each call auto-assigns a batch ID. All campaigns from the same call
        share a batch. Use repeat > 1 to run multiple independent trials.
        Each trial gets its own run_id and CPU allocation. Campaigns are
        queued when CPUs are exhausted.

        Args:
            fuzzer: Fuzzer name (e.g. 'aflplusplus')
            target: Target name (e.g. 'libpng')
            program: Program name from the target's configrc (e.g. 'libpng_read_fuzzer')
            args: Program launch arguments (e.g. '@@')
            fuzz_args: Extra arguments to pass to the fuzzer
            timeout: Campaign duration with suffix: s/m/h/d (default '1m')
            repeat: Number of independent campaign trials to run (default 1)
            num_cpus: CPUs to auto-allocate per campaign (0 = no affinity)
            poll: Seconds between monitor polls (default 5)
            no_archive: If true, move findings directly to ar/ instead of tarring (default false)
        """
        if fuzzer not in paths.list_fuzzer_names():
            return json.dumps({"error": f"Unknown fuzzer: {fuzzer}"})
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})

        image_name = f"magma/{fuzzer}/{target}"
        if not docker_utils.image_exists(image_name):
            return json.dumps({"error": f"Docker image not found: {image_name}. Build it first with magma_build_image."})

        if repeat < 1:
            return json.dumps({"error": "repeat must be >= 1"})

        batch_id = _next_batch_id()
        workdir = _get_workdir(batch_id)

        # Find the starting run_id based on existing runs
        ar_base = os.path.join(workdir, "ar", fuzzer, target, program)
        start_id = _next_run_id(ar_base)

        results = []
        for i in range(repeat):
            result = await _launch_one(
                fuzzer, target, program, args, timeout, poll,
                num_cpus, fuzz_args, workdir, run_id=start_id + i,
                no_archive=no_archive,
            )
            results.append(result)

        task_ids = [r["task_id"] for r in results if "task_id" in r]
        _batches[batch_id]["task_ids"].extend(task_ids)

        started = sum(1 for r in results if r.get("status") == "started")
        queued = sum(1 for r in results if r.get("status") == "queued")
        errors = sum(1 for r in results if "error" in r)

        return json.dumps({
            "batch_id": batch_id,
            "task_ids": task_ids,
            "started": started,
            "queued": queued,
            "errors": errors,
        })

    async def _stop_task(task_id: str) -> dict:
        """Stop a single task. Returns a status dict."""
        record = task_manager.get(task_id)
        if record is None:
            return {"task_id": task_id, "error": f"Task not found: {task_id}"}

        if record.status.value == "queued":
            await cpu_allocator.cancel_queued(task_id)
            record.status = TaskStatus.CANCELLED
            record.exit_code = -1
            record.finished_at = datetime.now(timezone.utc)
            return {"task_id": task_id, "status": "cancelled"}

        cancelled = await task_manager.cancel(task_id)
        if cancelled:
            return {"task_id": task_id, "status": "cancelled"}
        return {
            "task_id": task_id,
            "status": record.status.value,
            "message": "Task is not running (already finished or cancelled).",
        }

    @mcp.tool()
    async def magma_stop_campaign(
        batch_id: int,
        task_ids: list[str] | None = None,
    ) -> str:
        """Stop running campaigns by batch ID, optionally filtering by task IDs.

        If task_ids is provided, only those tasks are stopped. Otherwise, all
        tasks in the batch are stopped. Also releases any allocated CPUs and
        cancels queued requests.

        Args:
            batch_id: The batch_id returned by magma_start_campaign.
            task_ids: Optional list of specific task IDs to stop. If empty/null, stops all tasks in the batch.
        """
        if batch_id not in _batches:
            return json.dumps({"error": f"Batch not found: {batch_id}"})

        batch = _batches[batch_id]
        targets = task_ids if task_ids else batch["task_ids"]

        results = []
        for tid in targets:
            results.append(await _stop_task(tid))

        cancelled = sum(1 for r in results if r.get("status") == "cancelled")
        return json.dumps({
            "batch_id": batch_id,
            "cancelled": cancelled,
            "results": results,
        })

    @mcp.tool()
    async def magma_get_task_status(
        batch_id: int,
        task_ids: list[str] | None = None,
    ) -> str:
        """Check the status of campaign tasks by batch ID.

        If task_ids is provided, only those tasks are returned. Otherwise,
        all tasks in the batch are returned.

        Args:
            batch_id: The batch_id returned by magma_start_campaign.
            task_ids: Optional list of specific task IDs to check. If empty/null, returns all tasks in the batch.
        """
        if batch_id not in _batches:
            return json.dumps({"error": f"Batch not found: {batch_id}"})

        batch = _batches[batch_id]
        targets = task_ids if task_ids else batch["task_ids"]

        tasks = []
        for tid in targets:
            record = task_manager.get(tid)
            if record is None:
                tasks.append({"task_id": tid, "error": "Task not found"})
            else:
                tasks.append(record.to_dict())

        return json.dumps({"batch_id": batch_id, "tasks": tasks}, indent=2)

    @mcp.tool()
    async def magma_list_active_tasks() -> str:
        """List all active batches with their running/queued tasks."""
        batches = []
        for bid, batch in _batches.items():
            active = []
            for tid in batch["task_ids"]:
                record = task_manager.get(tid)
                if record and record.status in (TaskStatus.RUNNING, TaskStatus.QUEUED):
                    active.append(record.to_dict())
            if active:
                batches.append({
                    "batch_id": bid,
                    "tasks": active,
                    "count": len(active),
                })
        return json.dumps({"batches": batches, "total": sum(b["count"] for b in batches)}, indent=2)

    @mcp.tool()
    async def magma_configure_cpus(
        worker_mode: int = 0,
        max_cpus: int = 0,
    ) -> str:
        """Reconfigure the CPU pool for campaign affinity. Fails if any CPUs are allocated.

        Args:
            worker_mode: CPU dedup mode: 1=all logical CPUs, 2=one per physical core, 3=one per socket. 0 keeps current.
            max_cpus: Cap the pool to this many CPUs. 0 for no cap.
        """
        try:
            result = await cpu_allocator.reconfigure(
                worker_mode=worker_mode if worker_mode > 0 else None,
                max_cpus=max_cpus if max_cpus > 0 else None,
            )
        except RuntimeError as e:
            return json.dumps({"error": str(e)})
        return json.dumps({
            "old_pool_size": len(result["old_pool"]),
            "new_pool_size": len(result["new_pool"]),
            "new_pool": result["new_pool"],
        })

    @mcp.tool()
    async def magma_cpu_status() -> str:
        """Show CPU pool status: total, free, allocated per-task, and queued count."""
        status = cpu_allocator.status()
        # Enrich allocated entries with task descriptions
        enriched = {}
        for key, cpus in status["allocated"].items():
            record = task_manager.get(key)
            enriched[key] = {
                "cpus": cpus,
                "description": record.description if record else "unknown",
                "status": record.status.value if record else "unknown",
            }
        status["allocated"] = enriched
        return json.dumps(status, indent=2)
