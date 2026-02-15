#!/usr/bin/env python3
"""Target-specific release generation built on generic releasegen core."""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .core import (
    compute_cycle_end_year,
    ensure_repo_cache,
    get_first_commit_of_year,
    get_year_to_tag,
)


@dataclass(frozen=True)
class RepoSpec:
    name: str
    url: str


def parse_configrc_repo(configrc_path: Path) -> str | None:
    """Read TARGET_REPO from a bash-like configrc file."""
    if not configrc_path.is_file():
        return None
    for raw in configrc_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith("TARGET_REPO="):
            continue
        value = line.split("=", 1)[1].strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return value or None
    return None


def load_target_repo_specs(
    targets_dir: Path,
) -> list[RepoSpec]:
    """Load per-target repo URLs from configrc."""
    specs: list[RepoSpec] = []
    for target_dir in sorted(p for p in targets_dir.iterdir() if p.is_dir()):
        name = target_dir.name
        repo = parse_configrc_repo(target_dir / "configrc")
        if not repo:
            raise ValueError(f"No TARGET_REPO found in {target_dir / 'configrc'}")
        specs.append(RepoSpec(name=name, url=repo))
    return specs


def resolve_target_repo_spec(
    targets_dir: Path,
    target: str,
) -> RepoSpec:
    """Resolve one target to a RepoSpec for MCP-facing single-target actions."""
    target_dir = targets_dir / target
    if not target_dir.is_dir():
        raise ValueError(f"Unknown target: {target}")

    repo = parse_configrc_repo(target_dir / "configrc")
    if not repo:
        raise ValueError(f"No repo configured for target: {target}")
    return RepoSpec(name=target, url=repo)


def build_releases_lines(
    target_name: str,
    repo_url: str,
    start_year: int,
    end_year: int,
    stable_commit: str,
    year_to_tag: dict[int, str],
) -> list[str]:
    lines = [
        f'{target_name}_PIONEER="{repo_url}"\n',
        f'{target_name}_PIONEER_STABLE_COMMIT="{stable_commit}"\n',
    ]
    for year in range(start_year, end_year):
        lines.append(f'{target_name}_LEGACY_{year}="{repo_url}"\n')
        if year in year_to_tag:
            lines.append(f'{target_name}_LEGACY_{year}_TAG="{year_to_tag[year]}"\n')
    return lines


def write_target_releases(
    target_dir: Path,
    target_name: str,
    lines: list[str],
) -> Path:
    releases_path = target_dir / "releases"
    releases_path.write_text("".join(lines))
    return releases_path


def generate_target_release(
    magma_root: Path,
    target: str,
    start_year: int,
    dry_run: bool = False,
) -> dict:
    """Generate releases for one target and return MCP-friendly metadata."""
    targets_dir = magma_root / "targets"
    end_year = compute_cycle_end_year(start_year)
    spec = resolve_target_repo_spec(targets_dir, target)

    cache_root = Path(tempfile.mkdtemp(prefix="magma_releasegen_"))
    try:
        repo_path = ensure_repo_cache(spec.url, cache_root)
        stable = get_first_commit_of_year(repo_path, end_year)
        tags = get_year_to_tag(repo_path, end_year)
        lines = build_releases_lines(
            target_name=spec.name,
            repo_url=spec.url,
            start_year=start_year,
            end_year=end_year,
            stable_commit=stable,
            year_to_tag=tags,
        )
        releases_path = targets_dir / spec.name / "releases"
        if not dry_run:
            releases_path = write_target_releases(
                targets_dir / spec.name, spec.name, lines
            )
    finally:
        shutil.rmtree(cache_root, ignore_errors=True)

    return {
        "target": spec.name,
        "repo_url": spec.url,
        "start_year": start_year,
        "end_year": end_year,
        "stable_commit": stable,
        "releases_path": str(releases_path),
        "dry_run": dry_run,
        "releases_preview": "".join(lines),
    }


def generate_target_releases(
    magma_root: Path,
    start_year: int,
) -> list[Path]:
    """Generate releases files for all targets discoverable in magma/targets."""
    targets_dir = magma_root / "targets"
    end_year = compute_cycle_end_year(start_year)
    specs = load_target_repo_specs(targets_dir)

    created: list[Path] = []
    cache_root = Path(tempfile.mkdtemp(prefix="magma_releasegen_"))
    try:
        for spec in specs:
            repo_path = ensure_repo_cache(spec.url, cache_root)
            stable = get_first_commit_of_year(repo_path, end_year)
            tags = get_year_to_tag(repo_path, end_year)
            lines = build_releases_lines(
                target_name=spec.name,
                repo_url=spec.url,
                start_year=start_year,
                end_year=end_year,
                stable_commit=stable,
                year_to_tag=tags,
            )
            created.append(write_target_releases(targets_dir / spec.name, spec.name, lines))
    finally:
        shutil.rmtree(cache_root, ignore_errors=True)

    return created
