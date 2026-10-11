import asyncio

import pytest

from mmcp.core.cpu_allocator import CpuAllocator, _detect_cpus


def test_allocate_and_release():
    alloc = CpuAllocator(cpu_list=[0, 1, 2, 3])
    assert asyncio.run(alloc.allocate(2, "t1")) == [0, 1]
    assert asyncio.run(alloc.allocate(3, "t2")) is None
    asyncio.run(alloc.release("t1"))
    assert asyncio.run(alloc.allocate(3, "t3")) == [0, 1, 2]


def test_available_and_status():
    alloc = CpuAllocator(cpu_list=[0, 1])
    asyncio.run(alloc.allocate(1, "t1"))
    assert alloc.available() == [1]
    st = alloc.status()
    assert st["pool_size"] == 2
    assert st["free"] == [1]
    assert st["allocated"] == {"t1": [0]}
    assert st["allocated_count"] == 1
    assert st["queued_count"] == 0


def test_allocate_more_than_pool():
    alloc = CpuAllocator(cpu_list=[0])
    assert asyncio.run(alloc.allocate(2, "t1")) is None


def test_release_unknown_key():
    alloc = CpuAllocator(cpu_list=[0])
    asyncio.run(alloc.release("nobody"))
    assert alloc.status()["free_count"] == 1


def test_reconfigure_fails_while_allocated():
    alloc = CpuAllocator(cpu_list=[0, 1])
    asyncio.run(alloc.allocate(1, "t1"))
    with pytest.raises(RuntimeError):
        asyncio.run(alloc.reconfigure(max_cpus=1))


def test_reconfigure_caps_pool():
    alloc = CpuAllocator(cpu_list=[0, 1, 2, 3])
    res = asyncio.run(alloc.reconfigure(max_cpus=2))
    assert res["old_pool"] == [0, 1, 2, 3]
    assert res["new_pool"] == [0, 1]


def test_enqueue_and_cancel():
    alloc = CpuAllocator(cpu_list=[0])
    asyncio.run(alloc.allocate(1, "t1"))
    req = asyncio.run(alloc.enqueue(1, "t2"))
    assert asyncio.run(alloc.cancel_queued("t2")) is True
    assert req.cancelled is True
    assert asyncio.run(alloc.cancel_queued("nobody")) is False
    assert alloc.status()["queued_count"] == 0


def test_queue_fulfilled_on_release():
    alloc = CpuAllocator(cpu_list=[0, 1])
    asyncio.run(alloc.allocate(2, "t1"))
    req = asyncio.run(alloc.enqueue(2, "t2"))

    async def flow():
        loop = asyncio.get_running_loop()
        loop.call_later(
            0.05, lambda: asyncio.ensure_future(alloc.release("t1"))
        )
        await asyncio.wait_for(req.event.wait(), timeout=5)

    asyncio.run(flow())
    assert req.cancelled is False
    assert req.allocated_cpus == [0, 1]


def test_detect_cpus_dedup_modes(monkeypatch):
    class R:
        returncode = 0
        stdout = (
            "# CPU,Core,Socket\n"
            "0,0,0\n1,0,0\n2,1,1\n3,1,1\n4,2,0\n"
        )
        stderr = ""

    monkeypatch.setattr(
        "mmcp.core.cpu_allocator.subprocess.run", lambda *a, **k: R()
    )
    assert _detect_cpus(worker_mode=1) == [0, 1, 2, 3, 4]
    assert _detect_cpus(worker_mode=2) == [0, 2, 4]
    assert _detect_cpus(worker_mode=3) == [0, 2]
