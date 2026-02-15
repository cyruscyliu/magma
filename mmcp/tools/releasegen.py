"""Release generation tools: generate target releases from repo metadata."""

import json

from mcp.server.fastmcp import FastMCP

from ..core import paths
from tools.releasegen.targets import generate_target_release


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_generate_target_release(
        target: str,
        start_year: int = 2022,
    ) -> str:
        """Generate releases file for one target based on TARGET_REPO metadata.

        Writes `targets/{target}/releases` and returns generation metadata
        including resolved stable commit.

        Args:
            target: Target name (e.g. 'libpng').
            start_year: Baseline year for LEGACY entries (default 2022).
        """
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})
        if start_year < 2000 or start_year > 2100:
            return json.dumps({"error": f"Invalid start_year: {start_year}"})

        try:
            result = generate_target_release(
                magma_root=paths.MAGMA_ROOT,
                target=target,
                start_year=start_year,
            )
        except Exception as exc:
            return json.dumps({"error": str(exc)})

        return json.dumps(result, indent=2)
