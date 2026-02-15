"""Build tools: build Docker images for fuzzer/target combinations."""

import asyncio
import json

from mcp.server.fastmcp import FastMCP

from ..core import docker_utils, paths
from ..core.task_manager import TaskType, task_manager


def _make_build_env(
    fuzzer: str,
    target: str,
    target_version: str = "PIONEER",
    canary_mode: int = 1,
    isan: bool = False,
    harden: bool = False,
    source_coverage: bool = False,
) -> dict[str, str]:
    """Build the environment dict for a build.sh invocation."""
    env = {
        "FUZZER": fuzzer,
        "TARGET": target,
        "TARGET_VERSION": target_version,
        "CANARY_MODE": str(canary_mode),
        "MAGMA": str(paths.MAGMA_ROOT),
    }
    if isan:
        env["ISAN"] = "1"
    if harden:
        env["HARDEN"] = "1"
    if source_coverage:
        env["SOURCE_COVERAGE"] = "1"
    return env


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_build_image(
        fuzzer: str,
        target: str,
        target_version: str = "PIONEER",
        canary_mode: int = 1,
        isan: bool = False,
        harden: bool = False,
        source_coverage: bool = False,
    ) -> str:
        """Build a Docker image for a fuzzer/target combination. Returns a task_id for tracking (async operation).

        Args:
            fuzzer: Fuzzer name (e.g. 'aflplusplus', 'honggfuzz')
            target: Target name (e.g. 'libpng', 'libtiff')
            target_version: Version from releases file (default 'PIONEER')
            canary_mode: 1=with canaries, 2=no canaries, 3=with fixes (default 1)
            isan: Enable fatal canaries (default false)
            harden: Enable hardened canaries (default false)
            source_coverage: Enable source coverage instrumentation (default false)
        """
        if fuzzer not in paths.list_fuzzer_names():
            return json.dumps({"error": f"Unknown fuzzer: {fuzzer}"})
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})
        if canary_mode not in (1, 2, 3):
            return json.dumps({"error": f"Invalid canary_mode: {canary_mode}. Must be 1, 2, or 3."})

        env = _make_build_env(fuzzer, target, target_version, canary_mode, isan, harden, source_coverage)
        image_name = f"magma/{fuzzer}/{target}"
        record = await task_manager.spawn(
            task_type=TaskType.BUILD,
            description=f"build {image_name}",
            cmd=["bash", str(paths.BUILD_SH)],
            env=env,
            cwd=str(paths.MAGMA_ROOT),
        )

        return json.dumps({
            "task_id": record.task_id,
            "image_name": image_name,
            "status": "started",
        })

    @mcp.tool()
    async def magma_build_target_check_image(
        fuzzer: str,
        target: str,
        target_version: str = "PIONEER",
        canary_mode: int = 1,
        isan: bool = False,
        harden: bool = False,
        source_coverage: bool = False,
    ) -> str:
        """Build a reduced-context Docker image for target build verification.

        This is intended for ByteFuse task2 "update targets" verification loops.
        It uses tools/captain/build_target_check.sh which constructs a minimal
        Docker build context (skipping corpus/PoCs) and builds via
        docker/Dockerfile.target.build.
        """
        if fuzzer not in paths.list_fuzzer_names():
            return json.dumps({"error": f"Unknown fuzzer: {fuzzer}"})
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})
        if canary_mode not in (1, 2, 3):
            return json.dumps({"error": f"Invalid canary_mode: {canary_mode}. Must be 1, 2, or 3."})

        env = _make_build_env(fuzzer, target, target_version, canary_mode, isan, harden, source_coverage)
        image_name = f"magma-check/{fuzzer}/{target}"
        record = await task_manager.spawn(
            task_type=TaskType.BUILD,
            description=f"build-check {image_name}",
            cmd=["bash", str(paths.BUILD_TARGET_CHECK_SH)],
            env=env,
            cwd=str(paths.MAGMA_ROOT),
        )

        return json.dumps({
            "task_id": record.task_id,
            "image_name": image_name,
            "status": "started",
        })

    @mcp.tool()
    async def magma_build_images(
        fuzzers: list[str] | None = None,
        targets: list[str] | None = None,
        max_parallel: int = 2,
        target_version: str = "PIONEER",
        canary_mode: int = 1,
        isan: bool = False,
        harden: bool = False,
        source_coverage: bool = False,
    ) -> str:
        """Build Docker images for multiple fuzzer/target combinations with concurrency control.

        Queues all fuzzer×target builds and runs up to max_parallel at a time.
        Returns immediately with task_ids for all builds.

        Args:
            fuzzers: List of fuzzer names. Empty or null for all fuzzers.
            targets: List of target names. Empty or null for all targets.
            max_parallel: Maximum concurrent builds (default 2)
            target_version: Version from releases file (default 'PIONEER')
            canary_mode: 1=with canaries, 2=no canaries, 3=with fixes (default 1)
            isan: Enable fatal canaries (default false)
            harden: Enable hardened canaries (default false)
            source_coverage: Enable source coverage instrumentation (default false)
        """
        if canary_mode not in (1, 2, 3):
            return json.dumps({"error": f"Invalid canary_mode: {canary_mode}. Must be 1, 2, or 3."})

        all_fuzzers = paths.list_fuzzer_names()
        all_targets = paths.list_target_names()

        selected_fuzzers = fuzzers if fuzzers else all_fuzzers
        selected_targets = targets if targets else all_targets

        # Validate
        for f in selected_fuzzers:
            if f not in all_fuzzers:
                return json.dumps({"error": f"Unknown fuzzer: {f}"})
        for t in selected_targets:
            if t not in all_targets:
                return json.dumps({"error": f"Unknown target: {t}"})

        # Build the list of (fuzzer, target) pairs
        pairs = [(f, t) for f in selected_fuzzers for t in selected_targets]

        if not pairs:
            return json.dumps({"error": "No fuzzer/target combinations to build."})

        # Use a semaphore to limit concurrency
        sem = asyncio.Semaphore(max_parallel)

        async def spawn_build(fuzzer: str, target: str) -> dict:
            async with sem:
                env = _make_build_env(fuzzer, target, target_version, canary_mode, isan, harden, source_coverage)
                image_name = f"magma/{fuzzer}/{target}"
                record = await task_manager.spawn(
                    task_type=TaskType.BUILD,
                    description=f"build {image_name}",
                    cmd=["bash", str(paths.BUILD_SH)],
                    env=env,
                    cwd=str(paths.MAGMA_ROOT),
                )
                return {
                    "task_id": record.task_id,
                    "image_name": image_name,
                    "status": "started",
                }

        # Launch all builds with concurrency control
        coros = [spawn_build(f, t) for f, t in pairs]
        results = await asyncio.gather(*coros)

        return json.dumps({
            "total": len(results),
            "max_parallel": max_parallel,
            "tasks": list(results),
        })

    @mcp.tool()
    async def magma_get_task_log(
        task_id: str,
        tail: int = 0,
        search: str = "",
    ) -> str:
        """Retrieve the full log for a task from disk.

        Logs are persisted to mmcp/logs/{task_id}.log during execution.
        Use tail to get only the last N lines, or search to filter lines.

        Args:
            task_id: The task_id returned by an async tool
            tail: Only return the last N lines (0 = all)
            search: Filter to lines containing this string (e.g. 'error', 'FAILED')
        """
        record = task_manager.get(task_id)
        if record is None:
            return json.dumps({"error": f"Task not found: {task_id}"})

        lines = record.log_file.read_text().splitlines() if record.log_file.exists() else []
        total = len(lines)

        # Determine status from task record + log parsing for builds
        status = record.status.value
        if record.task_type == TaskType.BUILD and status in ("completed", "failed"):
            # Parse BuildKit log: last non-empty line is the image name on success
            # Errors show as "#N ERROR" lines
            has_error = any("ERROR" in l for l in lines)
            last_line = ""
            for l in reversed(lines):
                if l.strip():
                    last_line = l.strip()
                    break
            if has_error or not last_line.startswith(("magma/", "magma-check/")):
                status = "failed"
            else:
                status = "completed"

        if search:
            lines = [l for l in lines if search.lower() in l.lower()]
        if tail > 0:
            lines = lines[-tail:]

        return json.dumps({
            "task_id": task_id,
            "status": status,
            "total_lines": total,
            "returned_lines": len(lines),
            "log": "\n".join(lines),
        })

    @mcp.tool()
    async def magma_list_images() -> str:
        """List all built Magma Docker images."""
        try:
            images = docker_utils.list_magma_images()
        except RuntimeError as e:
            return json.dumps({"error": str(e)})

        return json.dumps({"images": images}, indent=2)
