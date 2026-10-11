import asyncio
import tarfile

import pytest

from mmcp.tools import campaign


@pytest.fixture(autouse=True)
def _batches_dir(magma_root, monkeypatch):
    monkeypatch.setattr(campaign, "_BATCHES_DIR", magma_root / "workdirs")
    campaign._batches.clear()


def test_get_workdir_creates_layout(magma_root):
    workdir = campaign._get_workdir("b1")
    for sub in ("ar", "cache", "log", "poc"):
        assert (magma_root / "workdirs" / "b1" / sub).is_dir()
    assert workdir.endswith("b1")
    assert campaign._batches["b1"]["task_ids"] == []


def test_get_workdir_idempotent(magma_root):
    campaign._get_workdir("b1")
    (magma_root / "workdirs" / "b1" / "ar" / "x").write_text("y")
    workdir = campaign._get_workdir("b1")
    assert (magma_root / "workdirs" / "b1" / "ar" / "x").exists()


def test_next_run_id(tmp_path):
    ar = tmp_path / "ar" / "x"
    assert campaign._next_run_id(str(ar)) == 0
    (ar / "0").mkdir(parents=True)
    assert campaign._next_run_id(str(ar)) == 1
    (ar / "3").mkdir()
    assert campaign._next_run_id(str(ar)) == 4


def test_archive_cache_move(tmp_path):
    src = tmp_path / "src"
    (src / "findings").mkdir(parents=True)
    (src / "findings" / "f").write_text("x")
    dst = tmp_path / "dst" / "run"
    campaign._archive_cache(str(src), str(dst), no_archive=True)
    assert not src.exists()
    assert (dst / "findings" / "f").exists()


def test_archive_cache_tar(tmp_path):
    src = tmp_path / "src"
    (src / "findings").mkdir(parents=True)
    (src / "findings" / "f").write_text("x")
    dst = tmp_path / "dst"
    campaign._archive_cache(str(src), str(dst), no_archive=False)
    assert not src.exists()
    assert (dst / "findings.tar").exists()
    with tarfile.open(dst / "findings.tar") as tf:
        names = [n.lstrip("./") for n in tf.getnames()]
        assert "findings/f" in names


def test_archive_cache_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        campaign._archive_cache(str(tmp_path / "nope"), str(tmp_path / "dst"), True)


def test_rebuild_batches(tmp_path, monkeypatch):
    from mmcp.core import task_manager as tm_mod
    from mmcp.core.task_manager import TaskType

    tasks_json = tmp_path / "tasks.json"
    monkeypatch.setattr("mmcp.core.task_manager.TASKS_JSON", tasks_json)

    async def flow():
        tm = tm_mod.task_manager
        rec = await tm.spawn(
            TaskType.CAMPAIGN, "c", ["true"],
            metadata={"batch_id": "b9"},
        )
        return rec

    rec = asyncio.run(flow())
    campaign._rebuild_batches()
    assert "b9" in campaign._batches
    assert rec.task_id in campaign._batches["b9"]["task_ids"]
