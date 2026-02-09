"""Patch management tools: read and update bug/setup patches."""

import json
import os

from mcp.server.fastmcp import FastMCP

from ..core import paths


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_get_patch(target: str, patch_name: str) -> str:
        """Read a bug patch or setup patch for a target.

        Args:
            target: Target name (e.g. 'libpng')
            patch_name: Patch filename without .patch extension (e.g. 'PNG001') or with extension
        """
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})

        # Strip .patch extension if provided
        if patch_name.endswith(".patch"):
            patch_name = patch_name[:-6]

        # Check bugs directory first, then setup
        bug_path = paths.target_bugs_dir(target) / f"{patch_name}.patch"
        setup_path = paths.target_setup_dir(target) / f"{patch_name}.patch"

        if bug_path.exists():
            return json.dumps({
                "target": target,
                "patch_name": patch_name,
                "type": "bug",
                "path": str(bug_path),
                "content": bug_path.read_text(),
            }, indent=2)
        elif setup_path.exists():
            return json.dumps({
                "target": target,
                "patch_name": patch_name,
                "type": "setup",
                "path": str(setup_path),
                "content": setup_path.read_text(),
            }, indent=2)
        else:
            available_bugs = paths.list_bug_ids(target)
            setup_dir = paths.target_setup_dir(target)
            available_setup = []
            if setup_dir.is_dir():
                available_setup = [p.stem for p in setup_dir.iterdir() if p.suffix == ".patch"]

            return json.dumps({
                "error": f"Patch '{patch_name}' not found for target '{target}'",
                "available_bugs": available_bugs,
                "available_setup": available_setup,
            })

    @mcp.tool()
    async def magma_update_patch(target: str, patch_name: str, content: str) -> str:
        """Write updated patch content for a bug or setup patch.

        Args:
            target: Target name (e.g. 'libpng')
            patch_name: Patch name without .patch extension (e.g. 'PNG001')
            content: New patch file content
        """
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})

        if patch_name.endswith(".patch"):
            patch_name = patch_name[:-6]

        # Determine if this is a bug or setup patch based on existing files
        bug_path = paths.target_bugs_dir(target) / f"{patch_name}.patch"
        setup_path = paths.target_setup_dir(target) / f"{patch_name}.patch"

        if bug_path.exists():
            target_path = bug_path
            patch_type = "bug"
        elif setup_path.exists():
            target_path = setup_path
            patch_type = "setup"
        else:
            # New patch: default to bugs directory
            os.makedirs(paths.target_bugs_dir(target), exist_ok=True)
            target_path = bug_path
            patch_type = "bug"

        target_path.write_text(content)

        return json.dumps({
            "success": True,
            "target": target,
            "patch_name": patch_name,
            "type": patch_type,
            "path": str(target_path),
        })
