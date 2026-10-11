import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from mmcp.core import paths


@pytest.fixture
def magma_root(tmp_path, monkeypatch):
    root = tmp_path / "magma"
    (root / "targets" / "libpng" / "patches" / "bugs").mkdir(parents=True)
    (root / "targets" / "libtiff" / "patches" / "bugs").mkdir(parents=True)
    (root / "fuzzers" / "aflplusplus").mkdir(parents=True)
    (root / "tools" / "captain").mkdir(parents=True)
    (root / "magma").mkdir(parents=True)
    (root / "targets" / "libpng" / "configrc").write_text(
        'PROGRAMS=(libpng_read_fuzzer)\nlibpng_read_fuzzer_ARGS="@@"\n'
    )
    (root / "targets" / "libtiff" / "configrc").write_text(
        'PROGRAMS=(tiff_read_rgba_fuzzer tiffcp)\ntiffcp_ARGS="-M @@ tmp.out"\n'
    )
    (root / "fuzzers" / "aflplusplus" / "run.sh").write_text("#!/bin/bash\n")
    (root / "targets" / "libpng" / "patches" / "bugs" / "PNG001.patch").write_text("x\n")
    (root / "targets" / "libpng" / "patches" / "bugs" / "PNG002.patch").write_text("y\n")

    monkeypatch.setattr(paths, "MAGMA_ROOT", root)
    monkeypatch.setattr(paths, "TARGETS_DIR", root / "targets")
    monkeypatch.setattr(paths, "FUZZERS_DIR", root / "fuzzers")
    monkeypatch.setattr(paths, "CAPTAIN_DIR", root / "tools" / "captain")
    monkeypatch.setattr(paths, "MAGMA_LIB_DIR", root / "magma")
    monkeypatch.setattr(paths, "CAPTAINRC", root / "tools" / "captain" / "captainrc")
    monkeypatch.setattr(paths, "LOG_DIR", root / "mmcp" / "logs")
    return root


@pytest.fixture
def tool_fn():
    def _get(mcp_instance, name):
        return mcp_instance._tool_manager._tools[name].fn

    return _get
