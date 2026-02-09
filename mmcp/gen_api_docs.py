#!/usr/bin/env python3
"""Auto-generate API documentation for the Magma MCP server.

Extracts tool schemas and resource URIs from the registered FastMCP server
and generates a Markdown reference document.

Usage:
    python -m mmcp.gen_api_docs                    # Print to stdout
    python -m mmcp.gen_api_docs > mmcp/API.md      # Write to file
"""

import json
import sys
from pathlib import Path

# Ensure project root is in path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mmcp.server import mcp


def generate_tool_docs() -> str:
    """Generate Markdown documentation for all registered tools."""
    lines = []
    lines.append("## Tools\n")

    tools = mcp._tool_manager._tools
    for name in sorted(tools.keys()):
        tool = tools[name]
        fn = tool.fn
        description = tool.description or fn.__doc__ or "No description."

        # Clean up description
        desc_lines = description.strip().splitlines()
        summary = desc_lines[0].strip()

        lines.append(f"### `{name}`\n")
        lines.append(f"{summary}\n")

        # Get the full docstring for args
        if fn.__doc__:
            doc = fn.__doc__.strip()
            # Find Args section
            if "Args:" in doc:
                args_section = doc.split("Args:")[1].strip()
                lines.append("**Parameters:**\n")
                for arg_line in args_section.splitlines():
                    arg_line = arg_line.strip()
                    if not arg_line:
                        break
                    if ":" in arg_line:
                        param, _, desc = arg_line.partition(":")
                        lines.append(f"- `{param.strip()}`: {desc.strip()}")
                lines.append("")

        # Get parameter schema from the tool
        schema = tool.parameters
        if schema and "properties" in schema:
            props = schema["properties"]
            required = set(schema.get("required", []))

            if props:
                lines.append("**Schema:**\n")
                lines.append("| Parameter | Type | Required | Default |")
                lines.append("|-----------|------|----------|---------|")
                for pname, pinfo in props.items():
                    ptype = pinfo.get("type", "any")
                    is_required = pname in required
                    default = pinfo.get("default", "—")
                    if default == "—" and not is_required:
                        default = "(optional)"
                    lines.append(
                        f"| `{pname}` | `{ptype}` | {'yes' if is_required else 'no'} | {default} |"
                    )
                lines.append("")

        lines.append("---\n")

    return "\n".join(lines)


def generate_resource_docs() -> str:
    """Generate Markdown documentation for all registered resources."""
    lines = []
    lines.append("## Resources\n")
    lines.append("Resources provide read-only data accessible via URI patterns.\n")

    # Static resources
    resources = mcp._resource_manager._resources
    if resources:
        lines.append("### Static Resources\n")
        lines.append("| URI | Description |")
        lines.append("|-----|-------------|")
        for uri in sorted(resources.keys()):
            res = resources[uri]
            fn = res.fn
            desc = fn.__doc__.strip().splitlines()[0] if fn.__doc__ else "—"
            lines.append(f"| `{uri}` | {desc} |")
        lines.append("")

    # Template resources
    templates = mcp._resource_manager._templates
    if templates:
        lines.append("### URI Templates\n")
        lines.append("| URI Pattern | Description |")
        lines.append("|-------------|-------------|")
        for uri in sorted(templates.keys()):
            tmpl = templates[uri]
            fn = tmpl.fn
            desc = fn.__doc__.strip().splitlines()[0] if fn.__doc__ else "—"
            lines.append(f"| `{uri}` | {desc} |")
        lines.append("")

    return "\n".join(lines)


def generate_full_docs() -> str:
    """Generate the complete API reference document."""
    lines = []
    lines.append("# Magma MCP Server — API Reference\n")
    lines.append(
        "*Auto-generated from server tool and resource registrations. "
        "Run `python -m mmcp.gen_api_docs` to regenerate.*\n"
    )
    lines.append("---\n")

    lines.append(generate_tool_docs())
    lines.append(generate_resource_docs())

    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_full_docs())
