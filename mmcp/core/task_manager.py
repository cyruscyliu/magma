"""Manage long-running async tasks (builds, campaigns, extractions).

Each task wraps an asyncio subprocess, tracks its status, and buffers
the last N lines of combined stdout/stderr for progress reporting.
Full logs are persisted to disk under mmcp/logs/.
"""

import asyncio
import os
import signal
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from . import paths


class TaskStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    BUILD = "build"
    CAMPAIGN = "campaign"
    EXTRACT = "extract"
    REPORT = "report"
    GENERIC = "generic"


@dataclass
class TaskRecord:
    task_id: str
    task_type: TaskType
    description: str
    status: TaskStatus = TaskStatus.RUNNING
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None
    exit_code: int | None = None
    output_buffer: deque = field(default_factory=lambda: deque(maxlen=200))
    log_file: Path | None = None
    _process: asyncio.subprocess.Process | None = field(default=None, repr=False)

    @property
    def elapsed_seconds(self) -> float:
        end = self.finished_at or datetime.now(timezone.utc)
        return (end - self.started_at).total_seconds()

    @property
    def output_tail(self) -> str:
        return "\n".join(self.output_buffer)

    def to_dict(self) -> dict:
        d = {
            "task_id": self.task_id,
            "type": self.task_type.value,
            "description": self.description,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "elapsed_seconds": round(self.elapsed_seconds, 1),
            "exit_code": self.exit_code,
            "output_tail": self.output_tail,
        }
        if self.log_file:
            d["log_file"] = str(self.log_file)
        return d


class TaskManager:
    """Singleton-style manager for tracking async subprocess tasks."""

    def __init__(self):
        self._tasks: dict[str, TaskRecord] = {}

    async def spawn(
        self,
        task_type: TaskType,
        description: str,
        cmd: list[str],
        env: dict[str, str] | None = None,
        cwd: str | None = None,
    ) -> TaskRecord:
        """Spawn a subprocess and track it as a task.

        Returns the TaskRecord immediately (task runs in background).
        """
        task_id = str(uuid.uuid4())

        # Create log directory and file
        paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = paths.LOG_DIR / f"{task_id}.log"

        merged_env = {**os.environ, **(env or {})}

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=merged_env,
            cwd=cwd,
        )

        record = TaskRecord(
            task_id=task_id,
            task_type=task_type,
            description=description,
            log_file=log_file,
            _process=process,
        )
        self._tasks[task_id] = record

        # Start background reader
        asyncio.create_task(self._read_output(record))

        return record

    async def _read_output(self, record: TaskRecord):
        """Read process output line by line into the circular buffer and log file."""
        process = record._process
        if process is None or process.stdout is None:
            return

        log_fh = None
        try:
            if record.log_file:
                log_fh = open(record.log_file, "w")

            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace").rstrip("\n")
                record.output_buffer.append(decoded)
                if log_fh:
                    log_fh.write(decoded + "\n")
                    log_fh.flush()
        except Exception:
            pass
        finally:
            if log_fh:
                log_fh.close()

        # Wait for process to finish
        exit_code = await process.wait()
        record.exit_code = exit_code
        record.status = TaskStatus.COMPLETED if exit_code == 0 else TaskStatus.FAILED
        record.finished_at = datetime.now(timezone.utc)

    def get(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)

    def list_active(self) -> list[TaskRecord]:
        return [t for t in self._tasks.values() if t.status == TaskStatus.RUNNING]

    def list_all(self) -> list[TaskRecord]:
        return list(self._tasks.values())

    def list_by_type(self, task_type: TaskType) -> list[TaskRecord]:
        return [t for t in self._tasks.values() if t.task_type == task_type]

    async def cancel(self, task_id: str) -> bool:
        """Cancel a running task by sending SIGTERM to its process."""
        record = self._tasks.get(task_id)
        if record is None or record.status != TaskStatus.RUNNING:
            return False

        process = record._process
        if process is None:
            return False

        try:
            process.send_signal(signal.SIGTERM)
            # Give it a moment to terminate gracefully
            try:
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
        except ProcessLookupError:
            pass

        record.status = TaskStatus.CANCELLED
        record.finished_at = datetime.now(timezone.utc)
        record.exit_code = -1
        return True


# Global singleton
task_manager = TaskManager()
