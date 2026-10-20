import json

import pytest

from mcp.server.fastmcp import FastMCP

from mmcp import server


def test_server_registers_tools_and_resources(magma_root):
    m = FastMCP("test")
    server.build.register(m)
    server.campaign.register(m)
    server.results.register(m)
    server.entity_files.register(m)

    tools = {t.name for t in __import__("asyncio").run(m.list_tools())}
    assert {
        "magma_build_image",
        "magma_start_campaign",
        "magma_stop_campaign",
        "magma_get_campaign_results",
        "magma_run_testcase",
        "magma_list_entity_files",
    } <= tools


def test_server_module_loads(magma_root):
    import asyncio

    tools = asyncio.run(server.mcp.list_tools())
    assert len(tools) >= 11


def test_http_client_example_exists(magma_root):
    from pathlib import Path

    example = Path(server.__file__).parent / "examples" / "http_client.py"
    assert example.is_file()
