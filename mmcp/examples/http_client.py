#!/usr/bin/env python3
"""Minimal Streamable HTTP MCP client for testing."""

import argparse
import json

import anyio

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MCP Streamable HTTP client")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/mcp/",
        help="MCP HTTP endpoint URL",
    )
    parser.add_argument(
        "--tool",
        default="magma_get_knowledge",
        help="Tool name to call",
    )
    parser.add_argument(
        "--args",
        default="{}",
        help="JSON object with tool arguments",
    )
    return parser.parse_args()


async def run(url: str, tool: str, args_json: str) -> None:
    arguments = json.loads(args_json)
    async with streamable_http_client(url) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, arguments)
            print(result)


def main() -> None:
    args = parse_args()
    anyio.run(run, args.url, args.tool, args.args)


if __name__ == "__main__":
    main()
