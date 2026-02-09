"""Discovery tools: list/inspect targets, fuzzers, and bugs."""

import json
import re

from mcp.server.fastmcp import FastMCP

from ..core import paths
from ..core.config_parser import parse_configrc, parse_releases


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_list_targets() -> str:
        """List all available fuzzing targets with their programs, bug IDs, and versions."""
        targets = []
        for name in paths.list_target_names():
            try:
                config = parse_configrc(name)
                versions = parse_releases(name)
            except Exception:
                config = {"programs": [], "program_args": {}}
                versions = []

            bug_ids = paths.list_bug_ids(name)

            targets.append({
                "name": name,
                "programs": config["programs"],
                "bug_ids": bug_ids,
                "bug_count": len(bug_ids),
                "versions": [v["name"] for v in versions],
            })

        return json.dumps({"targets": targets}, indent=2)

    @mcp.tool()
    async def magma_get_target_info(target: str) -> str:
        """Get detailed information about a specific target including programs, args, versions, bugs, and corpus sizes.

        Args:
            target: Target name (e.g. 'libpng', 'libtiff')
        """
        if target not in paths.list_target_names():
            return json.dumps({"error": f"Unknown target: {target}"})

        config = parse_configrc(target)
        versions = parse_releases(target)
        bug_ids = paths.list_bug_ids(target)
        poc_files = paths.list_poc_files(target)
        poc_bugs = {p.split(".")[0] for p in poc_files}

        programs = []
        for prog in config["programs"]:
            programs.append({
                "name": prog,
                "args": config["program_args"].get(prog, ""),
            })

        bugs = []
        for bid in bug_ids:
            bugs.append({
                "id": bid,
                "has_poc": bid in poc_bugs,
            })

        corpus_counts = {}
        for prog in config["programs"]:
            corpus_counts[prog] = len(paths.list_corpus_files(target, prog))

        return json.dumps({
            "name": target,
            "programs": programs,
            "versions": versions,
            "bugs": bugs,
            "corpus_counts": corpus_counts,
        }, indent=2)

    @mcp.tool()
    async def magma_list_fuzzers() -> str:
        """List all available fuzzers with their script files."""
        fuzzers = []
        for name in paths.list_fuzzer_names():
            fdir = paths.fuzzer_dir(name)
            scripts = sorted(
                p.name for p in fdir.iterdir()
                if p.is_file() and p.suffix == ".sh"
            )
            fuzzers.append({
                "name": name,
                "scripts": scripts,
            })

        return json.dumps({"fuzzers": fuzzers}, indent=2)

    @mcp.tool()
    async def magma_list_bugs(target: str = "") -> str:
        """List all bugs across all targets, or filtered to a specific target.

        Args:
            target: Optional target name to filter by (e.g. 'libpng'). Empty string for all targets.
        """
        targets = [target] if target else paths.list_target_names()
        bugs = []

        for t in targets:
            if t not in paths.list_target_names():
                continue
            poc_files = paths.list_poc_files(t)
            poc_bugs = {p.split(".")[0] for p in poc_files}

            for bid in paths.list_bug_ids(t):
                bugs.append({
                    "target": t,
                    "bug_id": bid,
                    "has_poc": bid in poc_bugs,
                })

        return json.dumps({"bugs": bugs, "total": len(bugs)}, indent=2)

    @mcp.tool()
    async def magma_get_bug_patch(target: str, bug_id: str) -> str:
        """Read the full patch content for a specific bug.

        Args:
            target: Target name (e.g. 'libpng')
            bug_id: Bug identifier (e.g. 'PNG001')
        """
        patch_path = paths.bug_patch_path(target, bug_id)
        if not patch_path.exists():
            return json.dumps({"error": f"Patch not found: {target}/{bug_id}"})

        content = patch_path.read_text()

        # Extract affected files from diff headers
        affected_files = re.findall(r"^\+\+\+ [ab]/(.+)$", content, re.MULTILINE)

        return json.dumps({
            "target": target,
            "bug_id": bug_id,
            "patch_content": content,
            "affected_files": list(set(affected_files)),
        }, indent=2)
