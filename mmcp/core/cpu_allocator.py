"""CPU affinity allocator for fuzzing campaigns.

Tracks a pool of available CPU IDs and allocates/releases them for
campaign containers. When CPUs aren't available, requests are queued
and fulfilled automatically when CPUs are released.
"""

import asyncio
import subprocess
from dataclasses import dataclass, field


def _detect_cpus(worker_mode: int = 2) -> list[int]:
    """Detect online CPUs via lscpu, matching run.sh's WORKER_MODE.

    Args:
        worker_mode: Deduplication mode (matches run.sh WORKER_MODE):
            1 = all logical CPUs (no dedup)
            2 = one per physical core (skip hyperthreads) [default]
            3 = one per socket
    """
    result = subprocess.run(
        ["lscpu", "-b", "-p"],
        capture_output=True, text=True, check=True,
    )
    # Format: CPU,Core,Socket,Node,,L1d,L1i,L2,L3
    # Column indices: 0=CPU, 1=Core, 2=Socket
    dedup_col = {1: None, 2: 1, 3: 2}.get(worker_mode)
    seen = set()
    cpus = []
    for line in result.stdout.splitlines():
        if line.startswith("#"):
            continue
        fields = line.split(",")
        cpu_id = int(fields[0])
        if dedup_col is not None:
            key = int(fields[dedup_col])
            if key in seen:
                continue
            seen.add(key)
        cpus.append(cpu_id)
    return sorted(cpus)


@dataclass
class _QueuedRequest:
    """A pending CPU allocation waiting for resources."""
    num_cpus: int
    key: str
    event: asyncio.Event = field(default_factory=asyncio.Event)
    allocated_cpus: list[int] = field(default_factory=list)
    cancelled: bool = False


class CpuAllocator:
    """Manages a pool of CPUs for campaign affinity binding."""

    def __init__(self, cpu_list: list[int] | None = None, worker_mode: int = 2):
        """Initialize the allocator.

        Args:
            cpu_list: Explicit list of CPU IDs to use. If None, auto-detect.
            worker_mode: CPU dedup mode (1=all, 2=per-core, 3=per-socket).
        """
        if cpu_list is not None:
            self._pool = set(cpu_list)
        else:
            self._pool = set(_detect_cpus(worker_mode=worker_mode))
        self._allocated: dict[str, set[int]] = {}
        self._waiters: list[_QueuedRequest] = []
        self._lock = asyncio.Lock()

    @property
    def pool_size(self) -> int:
        return len(self._pool)

    def _free_cpus(self) -> set[int]:
        used = set()
        for cpus in self._allocated.values():
            used |= cpus
        return self._pool - used

    async def allocate(self, n: int, key: str) -> list[int] | None:
        """Try to allocate n CPUs for the given key.

        Returns list of CPU IDs on success, None if not enough free.
        """
        async with self._lock:
            free = self._free_cpus()
            if len(free) < n:
                return None
            picked = sorted(free)[:n]
            self._allocated[key] = set(picked)
            return picked

    async def release(self, key: str) -> None:
        """Release CPUs held by key and process the wait queue."""
        async with self._lock:
            self._allocated.pop(key, None)
            await self._process_queue()

    async def _process_queue(self) -> None:
        """Fulfill queued requests that can now be satisfied. Must hold _lock."""
        still_waiting = []
        for req in self._waiters:
            if req.cancelled:
                continue
            free = self._free_cpus()
            if len(free) >= req.num_cpus:
                picked = sorted(free)[:req.num_cpus]
                self._allocated[req.key] = set(picked)
                req.allocated_cpus = picked
                req.event.set()
            else:
                still_waiting.append(req)
        self._waiters = still_waiting

    async def enqueue(self, n: int, key: str) -> _QueuedRequest:
        """Enqueue a request for n CPUs. Returns a _QueuedRequest whose
        event will be set when CPUs are allocated."""
        req = _QueuedRequest(num_cpus=n, key=key)
        async with self._lock:
            self._waiters.append(req)
        return req

    async def cancel_queued(self, key: str) -> bool:
        """Cancel a queued request by key. Returns True if found and cancelled."""
        async with self._lock:
            for req in self._waiters:
                if req.key == key and not req.cancelled:
                    req.cancelled = True
                    req.event.set()  # unblock any waiter
                    return True
            return False

    async def reconfigure(
        self, worker_mode: int | None = None, max_cpus: int | None = None
    ) -> dict:
        """Reinitialize the CPU pool. Fails if any CPUs are currently allocated.

        Args:
            worker_mode: New dedup mode (1=all, 2=per-core, 3=per-socket). None keeps current.
            max_cpus: Cap the pool to this many CPUs. None or 0 for no cap.

        Returns:
            dict with old_pool and new_pool for confirmation.
        """
        async with self._lock:
            if self._allocated:
                raise RuntimeError(
                    f"Cannot reconfigure while {len(self._allocated)} task(s) "
                    f"have allocated CPUs. Stop them first."
                )
            old_pool = sorted(self._pool)
            if worker_mode is not None:
                new_cpus = _detect_cpus(worker_mode=worker_mode)
            else:
                new_cpus = sorted(self._pool)
            if max_cpus and max_cpus > 0:
                new_cpus = new_cpus[:max_cpus]
            self._pool = set(new_cpus)
            # Cancel all waiters since pool changed
            for req in self._waiters:
                req.cancelled = True
                req.event.set()
            self._waiters.clear()
            return {"old_pool": old_pool, "new_pool": sorted(self._pool)}

    def available(self) -> list[int]:
        """Return sorted list of free CPU IDs."""
        used = set()
        for cpus in self._allocated.values():
            used |= cpus
        return sorted(self._pool - used)

    def status(self) -> dict:
        """Return full status of the CPU pool."""
        free = self.available()
        allocated = {
            key: sorted(cpus) for key, cpus in self._allocated.items()
        }
        return {
            "pool": sorted(self._pool),
            "pool_size": len(self._pool),
            "free": free,
            "free_count": len(free),
            "allocated": allocated,
            "allocated_count": len(self._pool) - len(free),
            "queued_count": sum(1 for r in self._waiters if not r.cancelled),
        }


# Global singleton — auto-detects CPUs on import
cpu_allocator = CpuAllocator()
