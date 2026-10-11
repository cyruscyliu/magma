import asyncio
import json
from pathlib import Path

import pytest

from mcp.server.fastmcp import FastMCP

from mmcp.tools import entity_files


@pytest.fixture
def mcp_instance():
    m = FastMCP("test")
    entity_files.register(m)
    return m


def test_entity_root_types(magma_root):
    assert entity_files._entity_root("target", "libpng") == (
        magma_root / "targets" / "libpng"
    )
    assert entity_files._entity_root("fuzzer", "aflplusplus") == (
        magma_root / "fuzzers" / "aflplusplus"
    )
    assert entity_files._entity_root("magma", "ignored") == (
        magma_root / "magma"
    )


def test_entity_root_invalid(magma_root):
    with pytest.raises(ValueError):
        entity_files._entity_root("bogus", "x")
    with pytest.raises(ValueError):
        entity_files._entity_root("target", "nosuch")


def test_safe_entity_file_rejects_escape(magma_root):
    root = magma_root / "targets" / "libpng"
    assert entity_files._safe_entity_file(root, "configrc").is_file()
    with pytest.raises(ValueError):
        entity_files._safe_entity_file(root, "../libtiff/configrc")
    with pytest.raises(ValueError):
        entity_files._safe_entity_file(root, "/abs/path")
    with pytest.raises(ValueError):
        entity_files._safe_entity_file(root, "")


def test_validate_glob_rejects_bad_patterns(magma_root):
    assert entity_files._validate_glob(" patches/** ") == "patches/**"
    with pytest.raises(ValueError):
        entity_files._validate_glob("")
    with pytest.raises(ValueError):
        entity_files._validate_glob("/abs/**")
    with pytest.raises(ValueError):
        entity_files._validate_glob("a/../b/**")


def test_list_entity_files(magma_root, mcp_instance, tool_fn):
    fn = tool_fn(mcp_instance, "magma_list_entity_files")
    out = json.loads(
        asyncio.run(
            fn(entity_type="target", entity_name="libpng", glob="patches/bugs/*")
        )
    )
    assert out["count"] == 2
    assert out["files"] == [
        "patches/bugs/PNG001.patch",
        "patches/bugs/PNG002.patch",
    ]
    assert out["truncated"] is False


def test_list_entity_files_max_results(magma_root, mcp_instance, tool_fn):
    fn = tool_fn(mcp_instance, "magma_list_entity_files")
    out = json.loads(
        asyncio.run(
            fn(entity_type="target", entity_name="libpng", glob="patches/bugs/*", max_results=1)
        )
    )
    assert out["count"] == 1
    assert out["truncated"] is True
    out = json.loads(
        asyncio.run(
            fn(entity_type="target", entity_name="libpng", glob="patches/bugs/*", max_results=0)
        )
    )
    assert "error" in out


def test_read_entity_file(magma_root, mcp_instance, tool_fn):
    fn = tool_fn(mcp_instance, "magma_read_entity_file")
    out = json.loads(
        asyncio.run(
            fn(entity_type="target", entity_name="libpng", relpath="configrc")
        )
    )
    assert 'PROGRAMS=(libpng_read_fuzzer)' in out["content"]
    out = json.loads(
        asyncio.run(
            fn(entity_type="target", entity_name="libpng", relpath="missing.txt")
        )
    )
    assert "error" in out


def test_update_and_restore_entity_file(magma_root, mcp_instance, tool_fn):
    read_fn = tool_fn(mcp_instance, "magma_read_entity_file")
    update_fn = tool_fn(mcp_instance, "magma_update_entity_file")
    restore_fn = tool_fn(mcp_instance, "magma_restore_entity_file")

    configrc = magma_root / "targets" / "libpng" / "configrc"
    original = configrc.read_text()

    up = json.loads(
        asyncio.run(
            update_fn(
                entity_type="target", entity_name="libpng",
                relpath="configrc", content="NEW",
            )
        )
    )
    assert configrc.read_text() == "NEW"
    backup = Path(up["backup_path"])
    assert backup.read_text() == original

    asyncio.run(
        restore_fn(
            entity_type="target", entity_name="libpng",
            relpath="configrc", backup_path=str(backup),
        )
    )
    assert configrc.read_text() == original
    assert json.loads(asyncio.run(read_fn(entity_type="target", entity_name="libpng", relpath="configrc")))["content"] == original


def test_patch_entity_file(magma_root, mcp_instance, tool_fn):
    fn = tool_fn(mcp_instance, "magma_patch_entity_file")
    configrc = magma_root / "targets" / "libpng" / "configrc"
    original = configrc.read_text()

    out = json.loads(
        asyncio.run(
            fn(
                entity_type="target", entity_name="libpng",
                relpath="configrc",
                patch_text=json.dumps(
                    {"replace": [{"from": "libpng_read_fuzzer", "to": "X"}]}
                ),
            )
        )
    )
    assert out["rules_applied"] == 1
    assert "X" in configrc.read_text()
    configrc.write_text(original)
