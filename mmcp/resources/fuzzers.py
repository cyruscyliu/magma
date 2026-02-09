"""MCP Resources for fuzzers: browsable access to fuzzer data."""

import json

from mcp.server.fastmcp import FastMCP

from ..core import paths


def register(mcp: FastMCP):
    @mcp.resource("magma://fuzzers")
    async def fuzzers_list() -> str:
        """List of all fuzzer names with available scripts."""
        fuzzers = []
        for name in paths.list_fuzzer_names():
            fdir = paths.fuzzer_dir(name)
            scripts = sorted(
                p.name for p in fdir.iterdir()
                if p.is_file() and p.suffix == ".sh"
            )
            fuzzers.append({"name": name, "scripts": scripts})
        return json.dumps(fuzzers, indent=2)

    @mcp.resource("magma://fuzzers/{fuzzer}")
    async def fuzzer_detail(fuzzer: str) -> str:
        """Fuzzer detail: scripts present, capabilities."""
        fdir = paths.fuzzer_dir(fuzzer)
        if not fdir.is_dir():
            return json.dumps({"error": f"Unknown fuzzer: {fuzzer}"})

        scripts = sorted(
            p.name for p in fdir.iterdir()
            if p.is_file() and p.suffix == ".sh"
        )

        # Identify capabilities
        capabilities = []
        if "run.sh" in scripts:
            capabilities.append("fuzzing")
        if "runonce.sh" in scripts:
            capabilities.append("single_input")
        if "findings.sh" in scripts:
            capabilities.append("crash_extraction")
        if "coverage.sh" in scripts:
            capabilities.append("coverage")
        if "instrument.sh" in scripts:
            capabilities.append("instrumentation")

        return json.dumps({
            "name": fuzzer,
            "scripts": scripts,
            "capabilities": capabilities,
        }, indent=2)

    @mcp.resource("magma://fuzzers/{fuzzer}/{script}")
    async def fuzzer_script(fuzzer: str, script: str) -> str:
        """Content of a specific fuzzer script."""
        path = paths.fuzzer_script(fuzzer, script)
        if not path.exists():
            return f"# Script not found: {fuzzer}/{script}"
        return path.read_text()
