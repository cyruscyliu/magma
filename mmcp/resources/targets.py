"""MCP Resources for targets: browsable access to target data."""

import json

from mcp.server.fastmcp import FastMCP

from ..core import paths
from ..core.config_parser import parse_configrc, parse_releases


def register(mcp: FastMCP):
    @mcp.resource("magma://targets")
    async def targets_list() -> str:
        """List of all target names with summary information."""
        targets = []
        for name in paths.list_target_names():
            try:
                config = parse_configrc(name)
            except Exception:
                config = {"programs": [], "program_args": {}}
            targets.append({
                "name": name,
                "programs": config["programs"],
                "bug_count": len(paths.list_bug_ids(name)),
            })
        return json.dumps(targets, indent=2)

    @mcp.resource("magma://targets/{target}")
    async def target_detail(target: str) -> str:
        """Full target detail: programs, args, versions, bugs, corpus counts."""
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

        bugs = [{"id": b, "has_poc": b in poc_bugs} for b in bug_ids]
        corpus = {p: len(paths.list_corpus_files(target, p)) for p in config["programs"]}

        return json.dumps({
            "name": target,
            "programs": programs,
            "versions": versions,
            "bugs": bugs,
            "corpus_counts": corpus,
        }, indent=2)

    @mcp.resource("magma://targets/{target}/configrc")
    async def target_configrc(target: str) -> str:
        """Raw configrc file content."""
        path = paths.target_configrc(target)
        if not path.exists():
            return f"# configrc not found for {target}"
        return path.read_text()

    @mcp.resource("magma://targets/{target}/releases")
    async def target_releases(target: str) -> str:
        """Raw releases file content."""
        path = paths.target_releases(target)
        if not path.exists():
            return f"# releases not found for {target}"
        return path.read_text()

    @mcp.resource("magma://targets/{target}/bugs")
    async def target_bugs(target: str) -> str:
        """List of bug IDs with has_poc flag."""
        bug_ids = paths.list_bug_ids(target)
        poc_files = paths.list_poc_files(target)
        poc_bugs = {p.split(".")[0] for p in poc_files}

        bugs = [{"id": b, "has_poc": b in poc_bugs} for b in bug_ids]
        return json.dumps(bugs, indent=2)

    @mcp.resource("magma://targets/{target}/bugs/{bug_id}")
    async def target_bug_patch(target: str, bug_id: str) -> str:
        """Raw patch file content for a specific bug."""
        path = paths.bug_patch_path(target, bug_id)
        if not path.exists():
            return f"# Patch not found: {target}/{bug_id}"
        return path.read_text()

    @mcp.resource("magma://targets/{target}/corpus/{program}")
    async def target_corpus(target: str, program: str) -> str:
        """List of seed file names for a program."""
        files = paths.list_corpus_files(target, program)
        return json.dumps(files, indent=2)
