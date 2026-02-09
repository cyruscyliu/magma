"""MCP Resources for configuration files."""

import json

from mcp.server.fastmcp import FastMCP

from ..core import paths, docker_utils


def register(mcp: FastMCP):
    @mcp.resource("magma://config/captainrc")
    async def captainrc_content() -> str:
        """Current captainrc configuration file content."""
        if not paths.CAPTAINRC.exists():
            return "# captainrc not found"
        return paths.CAPTAINRC.read_text()

    @mcp.resource("magma://docker/images")
    async def docker_images() -> str:
        """Currently built Magma Docker images."""
        try:
            images = docker_utils.list_magma_images()
        except RuntimeError:
            images = []
        return json.dumps(images, indent=2)
