"""Memory tools: retrieve Magma knowledge base and API documentation.

These tools allow AI agents to load contextual knowledge about Magma's
architecture, concepts, and MCP API before performing tasks.
"""

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

MMCP_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE = MMCP_DIR / "MAGMA_KNOWLEDGE_BASE.md"
API_DOCS = MMCP_DIR / "API.md"


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_get_knowledge(topic: str = "") -> str:
        """Retrieve Magma knowledge base documentation for understanding the benchmark.

        Returns the full knowledge base or a filtered section. Use this before
        performing complex tasks to understand Magma's architecture, environment
        variables, workflows, and conventions.

        Args:
            topic: Optional topic filter. Supported: 'canary', 'targets', 'fuzzers', 'docker', 'campaign', 'monitor', 'patches', 'captain', 'runonce', 'coverage', 'env', 'mcp'. Empty for full document.
        """
        if not KNOWLEDGE_BASE.exists():
            return json.dumps({"error": "Knowledge base not found."})

        content = KNOWLEDGE_BASE.read_text()

        if not topic:
            return content

        # Filter by topic — return relevant sections
        topic_lower = topic.lower()
        section_map = {
            "canary": ["## 5. Canary Instrumentation System"],
            "targets": ["## 6. Targets"],
            "fuzzers": ["## 7. Fuzzers"],
            "docker": ["## 3. Container Environment Variables", "## 4. Output Directories", "## 13. Docker Image Naming"],
            "campaign": ["## 8. Orchestration", "## 9. Campaign Workflow"],
            "monitor": ["## 10. Monitor Data Format"],
            "patches": ["## 6. Targets"],  # patches are part of targets section
            "captain": ["## 8. Orchestration"],
            "runonce": ["## 11. runonce.sh"],
            "coverage": ["## 4. Output Directories"],
            "env": ["## 3. Container Environment Variables"],
            "mcp": ["## 12. MCP Server"],
        }

        headers = section_map.get(topic_lower, [])
        if not headers:
            # Fallback: search for the topic in the content
            lines = content.splitlines()
            relevant = []
            capturing = False
            for line in lines:
                if topic_lower in line.lower():
                    capturing = True
                elif line.startswith("## ") and capturing:
                    capturing = False
                if capturing:
                    relevant.append(line)
            if relevant:
                return "\n".join(relevant)
            return f"No content found for topic: {topic}. Available topics: {', '.join(section_map.keys())}"

        # Extract matching sections
        lines = content.splitlines()
        result_lines = []
        capturing = False
        current_level = 0

        for line in lines:
            if any(line.startswith(h) for h in headers):
                capturing = True
                current_level = len(line) - len(line.lstrip("#"))
                result_lines.append(line)
            elif capturing:
                if line.startswith("## ") and not any(line.startswith(h) for h in headers):
                    capturing = False
                else:
                    result_lines.append(line)

        return "\n".join(result_lines) if result_lines else f"Section not found for topic: {topic}"

    @mcp.tool()
    async def magma_get_api_reference(tool_name: str = "") -> str:
        """Retrieve the MCP API reference documentation.

        Returns the full API reference or documentation for a specific tool.
        Use this to understand available tools, their parameters, and schemas.

        Args:
            tool_name: Optional specific tool name (e.g. 'magma_build_image'). Empty for full reference.
        """
        if not API_DOCS.exists():
            # Regenerate if missing
            try:
                from ..gen_api_docs import generate_full_docs
                content = generate_full_docs()
            except Exception:
                return json.dumps({"error": "API docs not found. Run: python -m mmcp.gen_api_docs > mmcp/API.md"})
        else:
            content = API_DOCS.read_text()

        if not tool_name:
            return content

        # Extract specific tool section
        lines = content.splitlines()
        result_lines = []
        capturing = False
        for line in lines:
            if line.strip() == f"### `{tool_name}`":
                capturing = True
            elif line.startswith("### ") and capturing:
                break
            if capturing:
                result_lines.append(line)

        if result_lines:
            return "\n".join(result_lines)
        return f"Tool not found: {tool_name}. Call with empty tool_name to see all tools."
