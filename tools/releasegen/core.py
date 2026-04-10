#!/usr/bin/env python3
"""Generic git/release generation primitives."""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


def compute_cycle_end_year(start_year: int) -> int:
    """Return cycle-aligned end year (e.g., 2025, 2028, 2031 for start=2022)."""
    current_year = datetime.now().year
    return start_year + (((current_year - start_year) // 3) * 3)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    out = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=True,
        capture_output=True,
        text=True,
    )
    return out.stdout


def ensure_repo_cache(repo_url: str, cache_root: Path) -> Path:
    cache_root.mkdir(parents=True, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = cache_root / repo_name
    if not repo_path.exists():
        run(["git", "clone", "--quiet", "--filter=blob:none", repo_url, str(repo_path)])
    else:
        run(["git", "fetch", "--quiet", "origin"], cwd=repo_path)
    return repo_path


def get_first_commit_of_year(repo_path: Path, year: int) -> str:
    start = f"{year}-01-01T00:00:00+0000"
    end = f"{year}-12-31T23:59:59+0000"
    out = run(
        [
            "git",
            "rev-list",
            "--reverse",
            f"--since={start}",
            f"--until={end}",
            "HEAD",
        ],
        cwd=repo_path,
    )
    commits = [x.strip() for x in out.splitlines() if x.strip()]
    if commits:
        return commits[0]

    # No commits in the target year — fall back to the most recent commit
    # before the end of that year (e.g. target has not been updated yet in 2026
    # but has commits from December 2025).
    out = run(
        [
            "git",
            "rev-list",
            f"--before={year + 1}-01-01T00:00:00+0000",
            "-1",
            "HEAD",
        ],
        cwd=repo_path,
    )
    fallback = out.strip()
    if not fallback:
        raise RuntimeError(f"No commits found up to year {year} for {repo_path.name}")
    return fallback


def get_year_to_tag(repo_path: Path, end_year: int) -> dict[int, str]:
    out = run(
        [
            "git",
            "for-each-ref",
            "--sort=creatordate",
            "--format=%(refname:strip=2)|%(creatordate:short)",
            "refs/tags",
        ],
        cwd=repo_path,
    )
    year_to_tag: dict[int, str] = {}
    for line in out.splitlines():
        if "|" not in line:
            continue
        tag, date = line.split("|", 1)
        if len(date) < 4:
            continue
        try:
            year = int(date[:4])
        except ValueError:
            continue
        if year not in year_to_tag:
            year_to_tag[year] = tag

    if not year_to_tag:
        raise RuntimeError(f"No tags found for {repo_path.name}")

    min_year = min(year_to_tag.keys())
    last_tag = ""
    for year in range(min_year, end_year):
        if year in year_to_tag:
            last_tag = year_to_tag[year]
        elif last_tag:
            year_to_tag[year] = last_tag
    return dict(sorted(year_to_tag.items()))
