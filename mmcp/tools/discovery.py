"""Discovery tools: list/inspect targets, fuzzers, and bugs."""

import json
import re

from mcp.server.fastmcp import FastMCP

from ..core import paths
from ..core.config_parser import parse_configrc, parse_releases


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_list_targets() -> str:
        """List all available fuzzing targets with programs, args, versions, bugs, and corpus sizes."""
        targets = []
        for name in paths.list_target_names():
            try:
                config = parse_configrc(name)
                versions = parse_releases(name)
            except Exception:
                config = {"programs": [], "program_args": {}}
                versions = []

            bug_ids = paths.list_bug_ids(name)
            poc_files = paths.list_poc_files(name)
            poc_bugs = {p.split(".")[0] for p in poc_files}

            programs = []
            for prog in config["programs"]:
                programs.append({
                    "name": prog,
                    "args": config["program_args"].get(prog, ""),
                    "corpus_count": len(paths.list_corpus_files(name, prog)),
                })

            bugs = []
            for bid in bug_ids:
                bugs.append({
                    "id": bid,
                    "has_poc": bid in poc_bugs,
                })

            targets.append({
                "name": name,
                "programs": programs,
                "versions": versions,
                "bugs": bugs,
            })

        return json.dumps({"targets": targets}, indent=2)

    @mcp.tool()
    async def magma_list_fuzzers() -> str:
        """List all available fuzzer names."""
        return json.dumps({"fuzzers": paths.list_fuzzer_names()}, indent=2)
