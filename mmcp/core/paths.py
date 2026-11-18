"""Path resolution for the Magma project root and standard subdirectories."""

import os
from pathlib import Path


def _find_magma_root() -> Path:
    """Resolve the Magma project root.

    Priority:
    1. MAGMA environment variable
    2. Walk up from this file: mcp/core/paths.py -> mcp/core -> mcp -> <root>
    """
    env = os.environ.get("MAGMA")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent.parent


MAGMA_ROOT = _find_magma_root()

TARGETS_DIR = MAGMA_ROOT / "targets"
FUZZERS_DIR = MAGMA_ROOT / "fuzzers"
CAPTAIN_DIR = MAGMA_ROOT / "tools" / "captain"
BENCHD_DIR = MAGMA_ROOT / "tools" / "benchd"
REPORT_DIR = MAGMA_ROOT / "tools" / "report_df"
DOCKER_DIR = MAGMA_ROOT / "docker"
MAGMA_LIB_DIR = MAGMA_ROOT / "magma"

CAPTAINRC = CAPTAIN_DIR / "captainrc"
DOCKERFILE = DOCKER_DIR / "Dockerfile"
TARGET_BUILD_DOCKERFILE = DOCKER_DIR / "Dockerfile.build"

BUILD_SH = CAPTAIN_DIR / "build.sh"
BUILD_TARGET_CHECK_SH = CAPTAIN_DIR / "build_check.py"
START_SH = CAPTAIN_DIR / "start.sh"
EXTRACT2_SH = CAPTAIN_DIR / "extract2.sh"
CAPTAIN_RUNONCE_SH = CAPTAIN_DIR / "runonce.sh"
RUNONCE_SH = MAGMA_LIB_DIR / "runonce.sh"

LOG_DIR = MAGMA_ROOT / "mmcp" / "logs"


def target_dir(target: str) -> Path:
    return TARGETS_DIR / target


def target_configrc(target: str) -> Path:
    return TARGETS_DIR / target / "configrc"


def target_releases(target: str) -> Path:
    return TARGETS_DIR / target / "releases"


def target_bugs_dir(target: str) -> Path:
    return TARGETS_DIR / target / "patches" / "bugs"


def target_setup_dir(target: str) -> Path:
    return TARGETS_DIR / target / "patches" / "setup"


def target_corpus_dir(target: str, program: str) -> Path:
    return TARGETS_DIR / target / "corpus" / program


def target_pocs_dir(target: str) -> Path:
    return TARGETS_DIR / target / "pocs"


def bug_patch_path(target: str, bug_id: str) -> Path:
    return target_bugs_dir(target) / f"{bug_id}.patch"


def fuzzer_dir(fuzzer: str) -> Path:
    return FUZZERS_DIR / fuzzer


def fuzzer_script(fuzzer: str, script: str) -> Path:
    return FUZZERS_DIR / fuzzer / script


def list_target_names() -> list[str]:
    """Return sorted list of target directory names."""
    if not TARGETS_DIR.is_dir():
        return []
    return sorted(
        d.name for d in TARGETS_DIR.iterdir()
        if d.is_dir() and (d / "configrc").exists()
    )


def list_fuzzer_names() -> list[str]:
    """Return sorted list of fuzzer directory names."""
    if not FUZZERS_DIR.is_dir():
        return []
    return sorted(
        d.name for d in FUZZERS_DIR.iterdir()
        if d.is_dir() and (d / "run.sh").exists()
    )


def list_bug_ids(target: str) -> list[str]:
    """Return sorted list of bug IDs for a target (e.g. ['PNG001', 'PNG002'])."""
    bugs_dir = target_bugs_dir(target)
    if not bugs_dir.is_dir():
        return []
    return sorted(
        p.stem for p in bugs_dir.iterdir()
        if p.suffix == ".patch"
    )


def list_poc_files(target: str) -> list[str]:
    """Return list of PoC file names for a target."""
    pocs_dir = target_pocs_dir(target)
    if not pocs_dir.is_dir():
        return []
    return sorted(p.name for p in pocs_dir.iterdir() if p.is_file())


def list_corpus_files(target: str, program: str) -> list[str]:
    """Return list of seed corpus file names."""
    corpus_dir = target_corpus_dir(target, program)
    if not corpus_dir.is_dir():
        return []
    return sorted(p.name for p in corpus_dir.iterdir() if p.is_file())
