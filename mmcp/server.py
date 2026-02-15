"""Magma Benchmark MCP Server.

Provides AI agents with tools and resources to control the Magma fuzzing
benchmark: inspect targets/fuzzers/bugs, build Docker images, run campaigns,
validate bug triggers, manage patches, and collect results.

Usage:
    # From the magma repo root:
    python -m mmcp

    # Or with FastMCP CLI (stdio transport):
    mcp run mmcp/server.py
"""

from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP(
    "magma-benchmark",
    instructions=(
        "Magma is a ground-truth fuzzing benchmark. Use the magma_* tools to "
        "inspect available targets and fuzzers, build Docker images, run fuzzing "
        "campaigns, test individual inputs for bug triggers, manage patches, and "
        "collect results. Long-running operations (builds, campaigns) return a "
        "task_id — poll with magma_get_task_status to check progress. "
        "Call magma_get_knowledge first to load context about Magma's architecture. "
        "Call magma_get_api_reference to see all available tools and parameters."
    ),
)

# Register all tool modules
from mmcp.tools import discovery, build, campaign, testing, results, patches

discovery.register(mcp)
build.register(mcp)
campaign.register(mcp)
testing.register(mcp)
results.register(mcp)
patches.register(mcp)

# Register all resource modules
from mmcp.resources import targets, fuzzers, config
from mmcp.resources import memory as memory_resources

targets.register(mcp)
fuzzers.register(mcp)
config.register(mcp)
memory_resources.register(mcp)


# ASGI app for uvicorn --reload
app = mcp.streamable_http_app()

if __name__ == "__main__":
    mcp.run()
