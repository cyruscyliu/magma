"""MCP Resources for knowledge base and API documentation."""

from pathlib import Path

from mcp.server.fastmcp import FastMCP

MMCP_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = MMCP_DIR / "MAGMA_KNOWLEDGE_BASE.md"
API_DOCS = MMCP_DIR / "API.md"


def register(mcp: FastMCP):
    @mcp.resource("magma://knowledge-base")
    async def knowledge_base() -> str:
        """Complete Magma knowledge base — architecture, concepts, env vars, workflows, conventions."""
        if not KNOWLEDGE_BASE.exists():
            return "# Knowledge base not found"
        return KNOWLEDGE_BASE.read_text()

    @mcp.resource("magma://api-reference")
    async def api_reference() -> str:
        """Auto-generated MCP API reference — all tools, parameters, schemas, and resources."""
        if not API_DOCS.exists():
            return "# API docs not found. Run: python -m mmcp.gen_api_docs > mmcp/API.md"
        return API_DOCS.read_text()
