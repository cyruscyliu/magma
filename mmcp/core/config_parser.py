"""Parse Magma's bash-based configuration files (configrc, releases, captainrc).

These files use bash syntax (arrays, variable assignments) and must be sourced
in a bash subprocess to be correctly interpreted.
"""

import asyncio
import re
import subprocess
from pathlib import Path

from .paths import (
    MAGMA_ROOT,
    TARGETS_DIR,
    target_configrc,
    target_releases,
    list_target_names,
)


def _run_bash(script: str, cwd: str | None = None) -> str:
    """Run a bash script and return stdout."""
    result = subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Bash script failed (rc={result.returncode}): {result.stderr.strip()}"
        )
    return result.stdout


def parse_configrc(target: str) -> dict:
    """Parse a target's configrc file.

    Returns:
        {
            "programs": ["prog1", "prog2"],
            "program_args": {"prog1": "args...", "prog2": ""}
        }
    """
    configrc = target_configrc(target)
    if not configrc.exists():
        raise FileNotFoundError(f"configrc not found for target {target}: {configrc}")

    script = f"""
source "{configrc}"
echo "PROGRAMS=${{PROGRAMS[@]}}"
for p in "${{PROGRAMS[@]}}"; do
    varname="${{p}}_ARGS"
    echo "${{p}}_ARGS=${{!varname}}"
done
"""
    output = _run_bash(script)

    programs = []
    program_args = {}

    for line in output.strip().splitlines():
        if line.startswith("PROGRAMS="):
            progs = line[len("PROGRAMS="):].strip()
            programs = progs.split() if progs else []
        elif "_ARGS=" in line:
            key, _, value = line.partition("=")
            prog_name = key.replace("_ARGS", "")
            program_args[prog_name] = value

    return {"programs": programs, "program_args": program_args}


def parse_releases(target: str) -> list[dict]:
    """Parse a target's releases file.

    Returns:
        [
            {"name": "PIONEER", "url": "https://...", "ref_type": "commit", "ref": "abc123"},
            {"name": "LEGACY_2024", "url": "https://...", "ref_type": "tag", "ref": "v1.0"},
        ]
    """
    releases_file = target_releases(target)
    if not releases_file.exists():
        return []

    content = releases_file.read_text()

    # Find all target-prefixed variable names
    # Pattern: <target>_<VERSION>="url" or <target>_<VERSION>_TAG/STABLE_COMMIT="ref"
    target_lower = target.replace("-", "_")

    # First pass: find all version names
    url_pattern = re.compile(
        rf'^{re.escape(target_lower)}_(\w+?)="([^"]*)"',
        re.MULTILINE,
    )
    tag_pattern = re.compile(
        rf'^{re.escape(target_lower)}_(\w+?)_TAG="([^"]*)"',
        re.MULTILINE,
    )
    commit_pattern = re.compile(
        rf'^{re.escape(target_lower)}_(\w+?)_STABLE_COMMIT="([^"]*)"',
        re.MULTILINE,
    )

    # Collect URLs (these define version names)
    versions: dict[str, dict] = {}
    for match in url_pattern.finditer(content):
        name, url = match.group(1), match.group(2)
        # Skip if this is a _TAG or _STABLE_COMMIT line
        if name.endswith("_TAG") or name.endswith("_STABLE_COMMIT"):
            continue
        versions[name] = {"name": name, "url": url, "ref_type": "", "ref": ""}

    # Fill in tags
    for match in tag_pattern.finditer(content):
        name, tag = match.group(1), match.group(2)
        if name in versions:
            versions[name]["ref_type"] = "tag"
            versions[name]["ref"] = tag

    # Fill in commits
    for match in commit_pattern.finditer(content):
        name, commit = match.group(1), match.group(2)
        if name in versions:
            versions[name]["ref_type"] = "commit"
            versions[name]["ref"] = commit

    # Sort: PIONEER first, then LEGACY_YYYY in reverse year order
    def sort_key(v: dict) -> tuple:
        name = v["name"]
        if name == "PIONEER":
            return (0, "")
        return (1, name)

    return sorted(versions.values(), key=sort_key)


def parse_captainrc(path: Path | None = None) -> dict:
    """Parse the captainrc configuration file.

    Returns dict with parsed configuration values.
    """
    from .paths import CAPTAINRC
    path = path or CAPTAINRC
    if not path.exists():
        raise FileNotFoundError(f"captainrc not found: {path}")

    script = f"""
source "{path}"
echo "WORKDIR=$WORKDIR"
echo "REPEAT=$REPEAT"
echo "TIMEOUT=$TIMEOUT"
echo "POLL=$POLL"
echo "CANARY_MODE=${{CANARY_MODE:-1}}"
echo "TARGET_VERSION=${{TARGET_VERSION:-PIONEER}}"
echo "FUZZERS=${{FUZZERS[@]}}"
echo "CAMPAIGN_WORKERS=${{CAMPAIGN_WORKERS:-1}}"
echo "WORKER_MODE=${{WORKER_MODE:-1}}"
echo "ISAN=$ISAN"
echo "HARDEN=$HARDEN"
echo "SOURCE_COVERAGE=$SOURCE_COVERAGE"
echo "CACHE_ON_DISK=$CACHE_ON_DISK"
echo "NO_ARCHIVE=$NO_ARCHIVE"
echo "TMPFS_SIZE=${{TMPFS_SIZE:-50g}}"
echo "POC_MODE=${{POC_MODE:-0}}"
echo "POC_EXTRACT=$POC_EXTRACT"
"""
    output = _run_bash(script)

    config = {}
    for line in output.strip().splitlines():
        key, _, value = line.partition("=")
        key = key.strip().lower()
        value = value.strip()
        if key == "fuzzers":
            config[key] = value.split() if value else []
        elif key in ("repeat", "poll", "canary_mode", "campaign_workers", "worker_mode", "poc_mode"):
            config[key] = int(value) if value else 0
        elif key in ("isan", "harden", "source_coverage", "cache_on_disk", "no_archive", "poc_extract"):
            config[key] = bool(value)
        else:
            config[key] = value

    return config


def get_all_targets_config() -> dict[str, dict]:
    """Parse configrc for all targets.

    Returns:
        {"libpng": {"programs": [...], "program_args": {...}}, ...}
    """
    result = {}
    for target in list_target_names():
        try:
            result[target] = parse_configrc(target)
        except Exception:
            continue
    return result
