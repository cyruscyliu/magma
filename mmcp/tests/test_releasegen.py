import datetime
import os
import subprocess

import pytest

from tools.releasegen import core as rg_core
from tools.releasegen import targets as rg_targets


def _make_repo(path, commit_date, tag=None):
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"], check=True)
    env = dict(os.environ, GIT_AUTHOR_DATE=commit_date, GIT_COMMITTER_DATE=commit_date)
    subprocess.run(
        ["git", "-C", str(path), "commit", "-q", "--allow-empty", "-m", "c1"],
        env=env, check=True,
    )
    if tag:
        subprocess.run(["git", "-C", str(path), "tag", tag], check=True)


def test_compute_cycle_end_year_covers_current_year():
    current = datetime.datetime.now().year
    end = rg_core.compute_cycle_end_year(2022)
    assert end == current + 1
    assert end - 1 == current


def test_compute_cycle_end_year_future_start(tmp_path):
    current = datetime.datetime.now().year
    assert rg_core.compute_cycle_end_year(current + 10) == current + 11


def test_get_first_commit_of_year(tmp_path):
    repo = tmp_path / "repo"
    _make_repo(repo, "2022-03-01T12:00:00")
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert rg_core.get_first_commit_of_year(repo, 2022) == head


def test_get_first_commit_of_year_no_commits(tmp_path):
    repo = tmp_path / "repo"
    _make_repo(repo, "2022-03-01T12:00:00")
    with pytest.raises(RuntimeError):
        rg_core.get_first_commit_of_year(repo, 2023)


def test_get_year_to_tag(tmp_path):
    repo = tmp_path / "repo"
    _make_repo(repo, "2022-03-01T12:00:00", tag="v2022")
    filled = rg_core.get_year_to_tag(repo, 2030)
    assert filled[2022] == "v2022"
    assert filled[2029] == "v2022"
    assert list(filled.keys()) == list(range(2022, 2030))


def test_get_year_to_tag_no_tags(tmp_path):
    repo = tmp_path / "repo"
    _make_repo(repo, "2022-03-01T12:00:00")
    with pytest.raises(RuntimeError):
        rg_core.get_year_to_tag(repo, 2030)


def test_ensure_repo_cache_clones_and_reuses(tmp_path):
    src = tmp_path / "src-repo"
    _make_repo(src, "2022-03-01T12:00:00")
    cache = tmp_path / "cache"
    p1 = rg_core.ensure_repo_cache(str(src), cache)
    assert (p1 / ".git").exists()
    p2 = rg_core.ensure_repo_cache(str(src), cache)
    assert p1 == p2


def test_build_releases_lines():
    lines = rg_targets.build_releases_lines(
        target_name="libpng",
        repo_url="https://example.com/libpng.git",
        start_year=2022,
        end_year=2027,
        stable_commit="head1",
        year_to_tag={2022: "v2022", 2024: "v2024"},
        first_commits={y: f"c{y}" for y in range(2022, 2027)},
    )
    text = "".join(lines)
    assert 'libpng_PIONEER="https://example.com/libpng.git"' in text
    assert 'libpng_PIONEER_STABLE_COMMIT="head1"' in text
    assert 'libpng_LEGACY_2022_TAG="v2022"' in text
    assert 'libpng_LEGACY_2024_TAG="v2024"' in text
    assert "libpng_LEGACY_2023_TAG" not in text
    assert 'libpng_LEGACY_2022_STABLE_COMMIT="c2022"' in text
    assert 'libpng_LEGACY_2026_STABLE_COMMIT="c2026"' in text


def test_parse_configrc_repo(tmp_path):
    rc = tmp_path / "configrc"
    rc.write_text('TARGET_REPO="https://example.com/x.git"\n\n# c\nOTHER=1\n')
    assert rg_targets.parse_configrc_repo(rc) == "https://example.com/x.git"
    assert rg_targets.parse_configrc_repo(tmp_path / "nope") is None


def test_load_target_repo_specs(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "configrc").write_text('TARGET_REPO="https://e.com/a.git"\n')
    (tmp_path / "b" / "configrc").write_text('TARGET_REPO="https://e.com/b.git"\n')
    specs = rg_targets.load_target_repo_specs(tmp_path)
    assert [(s.name, s.url) for s in specs] == [
        ("a", "https://e.com/a.git"),
        ("b", "https://e.com/b.git"),
    ]


def test_generate_target_release_dry_run(tmp_path):
    src = tmp_path / "upstream"
    _make_repo(src, "2022-03-01T12:00:00", tag="v2022")
    current = datetime.datetime.now().year
    env = dict(
        os.environ,
        GIT_AUTHOR_DATE=f"{current}-02-01T12:00:00",
        GIT_COMMITTER_DATE=f"{current}-02-01T12:00:00",
    )
    subprocess.run(
        ["git", "-C", str(src), "commit", "-q", "--allow-empty", "-m", "c2"],
        env=env, check=True,
    )
    (tmp_path / "targets" / "mytarget").mkdir(parents=True)
    (tmp_path / "targets" / "mytarget" / "configrc").write_text(
        f'TARGET_REPO="{src}"\n'
    )
    meta = rg_targets.generate_target_release(
        magma_root=tmp_path, target="mytarget", start_year=2022, dry_run=True
    )
    assert meta["target"] == "mytarget"
    assert meta["stable_commit"]
    assert "mytarget_PIONEER=" in meta["releases_preview"]
    assert not (tmp_path / "targets" / "mytarget" / "releases").exists()
