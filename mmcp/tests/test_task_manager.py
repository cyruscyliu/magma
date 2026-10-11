import json

from mmcp.core import task_manager


def _tasks_json(magma_root):
    return magma_root / "mmcp" / "logs" / "tasks.json"


def test_spawn_completes(magma_root, monkeypatch):
    monkeypatch.setattr(task_manager, "TASKS_JSON", _tasks_json(magma_root))

    async def flow():
        tm = task_manager.TaskManager()
        rec = await tm.spawn(
            task_manager.TaskType.BUILD, "echo", ["echo", "hi"]
        )
        loop = asyncio.get_running_loop()
        end = loop.time() + 10
        while rec.status != task_manager.TaskStatus.COMPLETED:
            await asyncio.sleep(0.02)
            assert loop.time() < end
        return rec

    rec = asyncio.run(flow())
    assert rec.exit_code == 0
    assert rec.log_file.exists()
    assert "hi" in rec.log_file.read_text()


def test_spawn_failing_cmd(magma_root, monkeypatch):
    monkeypatch.setattr(task_manager, "TASKS_JSON", _tasks_json(magma_root))

    async def flow():
        tm = task_manager.TaskManager()
        rec = await tm.spawn(task_manager.TaskType.BUILD, "fail", ["false"])
        loop = asyncio.get_running_loop()
        end = loop.time() + 10
        while rec.status != task_manager.TaskStatus.FAILED:
            await asyncio.sleep(0.02)
            assert loop.time() < end
        return rec

    rec = asyncio.run(flow())
    assert rec.status == task_manager.TaskStatus.FAILED
    assert rec.exit_code != 0


def test_cancel_running_task(magma_root, monkeypatch):
    monkeypatch.setattr(task_manager, "TASKS_JSON", _tasks_json(magma_root))

    async def flow():
        tm = task_manager.TaskManager()
        rec = await tm.spawn(
            task_manager.TaskType.CAMPAIGN, "sleep", ["sleep", "30"]
        )
        ok = await tm.cancel(rec.task_id)
        return ok, rec

    ok, rec = asyncio.run(flow())
    assert ok is True
    assert rec.status == task_manager.TaskStatus.CANCELLED
    assert rec.exit_code == -1


def test_cancel_nonexistent_or_stopped(magma_root, monkeypatch):
    monkeypatch.setattr(task_manager, "TASKS_JSON", _tasks_json(magma_root))
    tm = task_manager.TaskManager()
    import asyncio

    assert asyncio.run(tm.cancel("nobody")) is False


def test_persistence_running_becomes_failed(magma_root, monkeypatch):
    tasks_json = _tasks_json(magma_root)
    monkeypatch.setattr(task_manager, "TASKS_JSON", tasks_json)
    tasks_json.parent.mkdir(parents=True, exist_ok=True)
    tasks_json.write_text(
        json.dumps(
            [
                {
                    "task_id": "t-old",
                    "type": "build",
                    "description": "d",
                    "status": "running",
                    "started_at": "2026-01-01T00:00:00+00:00",
                    "finished_at": None,
                    "exit_code": None,
                    "log_file": str(magma_root / "x.log"),
                    "metadata": {"batch_id": "b1"},
                }
            ]
        )
    )

    tm = task_manager.TaskManager()
    rec = tm.get("t-old")
    assert rec is not None
    assert rec.status == task_manager.TaskStatus.FAILED
    assert rec.exit_code == -1
    assert tasks_json.exists()


def test_register_queued_and_start(magma_root, monkeypatch):
    monkeypatch.setattr(task_manager, "TASKS_JSON", _tasks_json(magma_root))

    async def flow():
        tm = task_manager.TaskManager()
        rec = tm.register_queued(
            task_manager.TaskType.REPORT, "queued job"
        )
        assert rec.status == task_manager.TaskStatus.QUEUED
        await tm.start_queued(rec, ["echo", "done"])
        loop = asyncio.get_running_loop()
        end = loop.time() + 10
        while rec.status != task_manager.TaskStatus.COMPLETED:
            await asyncio.sleep(0.02)
            assert loop.time() < end
        assert tm.list_by_type(task_manager.TaskType.REPORT)
        return rec

    rec = asyncio.run(flow())
    assert rec.exit_code == 0


def test_to_dict_roundtrip(magma_root, monkeypatch):
    monkeypatch.setattr(task_manager, "TASKS_JSON", _tasks_json(magma_root))
    rec = task_manager.TaskRecord(
        task_id="x",
        task_type=task_manager.TaskType.BUILD,
        description="d",
        status=task_manager.TaskStatus.COMPLETED,
    )
    d = rec.to_dict()
    assert d["task_id"] == "x"
    assert d["status"] == "completed"
    p = rec._to_persist()
    back = task_manager.TaskRecord._from_persist(p)
    assert back.task_id == rec.task_id
    assert back.status == rec.status


import asyncio
