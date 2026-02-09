"""Campaign tools: start/stop fuzzing campaigns, check task status."""

import json
import os
import tempfile

from mcp.server.fastmcp import FastMCP

from ..core import docker_utils, paths
from ..core.config_parser import parse_configrc
from ..core.task_manager import TaskType, task_manager


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_start_campaign(
        fuzzer: str,
        target: str,
        program: str,
        timeout: str = "1m",
        poll: int = 5,
        affinity: str = "",
        fuzz_args: str = "",
        workdir: str = "",
    ) -> str:
        """Start a single fuzzing campaign in a Docker container. Returns a task_id for tracking (async).

        The Docker image must already be built via magma_build_image.

        Args:
            fuzzer: Fuzzer name (e.g. 'aflplusplus')
            target: Target name (e.g. 'libpng')
            program: Program name from the target's configrc (e.g. 'libpng_read_fuzzer')
            timeout: Campaign duration with suffix: s/m/h/d (default '1m')
            poll: Seconds between monitor polls (default 5)
            affinity: CPU affinity, comma-separated core IDs (e.g. '0,1'). Empty for no affinity.
            fuzz_args: Extra arguments to pass to the fuzzer
            workdir: Where to store shared results. Auto-created if empty.
        """
        if fuzzer not in paths.list_fuzzer_names():
            return json.dumps({"error": f"Unknown fuzzer: {fuzzer}"})
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})

        image_name = f"magma/{fuzzer}/{target}"
        if not docker_utils.image_exists(image_name):
            return json.dumps({"error": f"Docker image not found: {image_name}. Build it first with magma_build_image."})

        # Validate program name
        try:
            config = parse_configrc(target)
        except Exception as e:
            return json.dumps({"error": f"Failed to parse configrc for {target}: {e}"})

        if program not in config["programs"]:
            return json.dumps({
                "error": f"Unknown program '{program}' for target '{target}'. Available: {config['programs']}"
            })

        # Get default args for this program
        args = config["program_args"].get(program, "")

        # Set up shared directory
        if not workdir:
            workdir = tempfile.mkdtemp(prefix=f"magma_{fuzzer}_{target}_{program}_")

        shared = os.path.join(workdir, "shared")
        os.makedirs(shared, exist_ok=True)

        env = {
            "FUZZER": fuzzer,
            "TARGET": target,
            "PROGRAM": program,
            "ARGS": args,
            "FUZZARGS": fuzz_args,
            "POLL": str(poll),
            "TIMEOUT": timeout,
            "SHARED": shared,
            "MAGMA": str(paths.MAGMA_ROOT),
        }
        if affinity:
            env["AFFINITY"] = affinity

        record = await task_manager.spawn(
            task_type=TaskType.CAMPAIGN,
            description=f"campaign {fuzzer}/{target}/{program}",
            cmd=["bash", str(paths.START_SH)],
            env=env,
            cwd=str(paths.MAGMA_ROOT),
        )

        return json.dumps({
            "task_id": record.task_id,
            "fuzzer": fuzzer,
            "target": target,
            "program": program,
            "workdir": workdir,
            "shared": shared,
            "status": "started",
        })

    @mcp.tool()
    async def magma_stop_campaign(task_id: str) -> str:
        """Stop a running campaign or any long-running task.

        Args:
            task_id: The task_id returned by magma_start_campaign, magma_build_image, etc.
        """
        record = task_manager.get(task_id)
        if record is None:
            return json.dumps({"error": f"Task not found: {task_id}"})

        cancelled = await task_manager.cancel(task_id)
        if cancelled:
            return json.dumps({"status": "cancelled", "task_id": task_id})
        else:
            return json.dumps({
                "status": record.status.value,
                "task_id": task_id,
                "message": "Task is not running (already finished or cancelled).",
            })

    @mcp.tool()
    async def magma_get_task_status(task_id: str) -> str:
        """Check the status of a long-running operation (build, campaign, extract, etc.).

        Args:
            task_id: The task_id returned by an async tool
        """
        record = task_manager.get(task_id)
        if record is None:
            return json.dumps({"error": f"Task not found: {task_id}"})

        return json.dumps(record.to_dict(), indent=2)

    @mcp.tool()
    async def magma_list_active_tasks() -> str:
        """List all currently running long-running operations."""
        active = task_manager.list_active()
        tasks = [t.to_dict() for t in active]
        return json.dumps({"tasks": tasks, "count": len(tasks)}, indent=2)
