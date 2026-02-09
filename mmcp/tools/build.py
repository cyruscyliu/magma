"""Build tools: build Docker images for fuzzer/target combinations."""

import json

from mcp.server.fastmcp import FastMCP

from ..core import docker_utils, paths
from ..core.task_manager import TaskManager, TaskType, task_manager


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
    async def magma_list_images() -> str:
        """List all built Magma Docker images."""
        try:
            images = docker_utils.list_magma_images()
        except RuntimeError as e:
            return json.dumps({"error": str(e)})

        return json.dumps({"images": images}, indent=2)
