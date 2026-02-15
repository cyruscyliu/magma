"""Manage long-running async tasks (builds, campaigns, extractions).

Each task wraps an asyncio subprocess, tracks its status, and buffers
the last N lines of combined stdout/stderr for progress reporting.
Full logs are persisted to disk under mmcp/logs/.
Task metadata is persisted to mmcp/logs/tasks.json so records survive
server reloads.
"""

import asyncio
import json
import os
import signal
import tempfile
import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from . import paths

TASKS_JSON = paths.LOG_DIR / "tasks.json"


class TaskStatus(str, Enum):
    QUEUED = "queued"
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
    log_file: Path = field(default_factory=lambda: paths.LOG_DIR / "unknown.log")
    metadata: dict = field(default_factory=dict)
    _process: asyncio.subprocess.Process | None = field(default=None, repr=False)
    _on_finish: Callable[["TaskRecord"], Awaitable[None]] | None = field(
        default=None, repr=False
    )

    @property
    def elapsed_seconds(self) -> float:
        end = self.finished_at or datetime.now(timezone.utc)
        return (end - self.started_at).total_seconds()

    def to_dict(self) -> dict:
        d = {
            "task_id": self.task_id,
            "type": self.task_type.value,
            "description": self.description,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "elapsed_seconds": round(self.elapsed_seconds, 1),
            "exit_code": self.exit_code,
            "log_file": str(self.log_file),
        }
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    def _to_persist(self) -> dict:
        """Full serialization for disk persistence (includes finished_at)."""
        return {
            "task_id": self.task_id,
            "type": self.task_type.value,
            "description": self.description,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "exit_code": self.exit_code,
            "log_file": str(self.log_file),
            "metadata": self.metadata,
        }

    @classmethod
    def _from_persist(cls, d: dict) -> "TaskRecord":
        """Reconstruct a TaskRecord from a persisted dict."""
        finished = None
        if d.get("finished_at"):
            finished = datetime.fromisoformat(d["finished_at"])
        return cls(
            task_id=d["task_id"],
            task_type=TaskType(d["type"]),
            description=d["description"],
            status=TaskStatus(d["status"]),
            started_at=datetime.fromisoformat(d["started_at"]),
            finished_at=finished,
            exit_code=d.get("exit_code"),
            log_file=Path(d["log_file"]),
            metadata=d.get("metadata", {}),
        )


class TaskManager:
    """Singleton-style manager for tracking async subprocess tasks."""

    def __init__(self):
        self._tasks: dict[str, TaskRecord] = {}
        self._load()

    def _save(self):
        """Persist all task records to disk (atomic write)."""
        paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
        data = [r._to_persist() for r in self._tasks.values()]
        fd, tmp = tempfile.mkstemp(dir=paths.LOG_DIR, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, TASKS_JSON)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass

    def _load(self):
        """Load persisted task records from disk.

        RUNNING/QUEUED tasks are marked FAILED since their processes
        are gone after a reload.
        """
        if not TASKS_JSON.exists():
            return
        try:
            data = json.loads(TASKS_JSON.read_text())
        except (json.JSONDecodeError, OSError):
            return
        for d in data:
            try:
                record = TaskRecord._from_persist(d)
                # Processes can't survive reload
                if record.status in (TaskStatus.RUNNING, TaskStatus.QUEUED):
                    record.status = TaskStatus.FAILED
                    record.finished_at = record.finished_at or datetime.now(timezone.utc)
                    record.exit_code = record.exit_code if record.exit_code is not None else -1
                self._tasks[record.task_id] = record
            except (KeyError, ValueError):
                continue
        # Re-save with corrected statuses
        self._save()

    async def spawn(
        self,
        task_type: TaskType,
        description: str,
        cmd: list[str],
        env: dict[str, str] | None = None,
        cwd: str | None = None,
        on_finish: Callable[[TaskRecord], Awaitable[None]] | None = None,
        metadata: dict | None = None,
        log_file: Path | None = None,
    ) -> TaskRecord:
        """Spawn a subprocess and track it as a task.

        Returns the TaskRecord immediately (task runs in background).
        """
        task_id = str(uuid.uuid4())

        if log_file is None:
            paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = paths.LOG_DIR / f"{task_id}.log"
        else:
            log_file.parent.mkdir(parents=True, exist_ok=True)

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
            metadata=metadata or {},
            _process=process,
            _on_finish=on_finish,
        )
        self._tasks[task_id] = record
        self._save()

        # Start background reader
        asyncio.create_task(self._read_output(record))

        return record

    async def _read_output(self, record: TaskRecord):
        """Read process output line by line into the log file."""
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
        self._save()

        if record._on_finish:
            try:
                await record._on_finish(record)
            except Exception:
                pass

    def register_queued(
        self,
        task_type: TaskType,
        description: str,
        on_finish: Callable[[TaskRecord], Awaitable[None]] | None = None,
        metadata: dict | None = None,
        log_file: Path | None = None,
    ) -> TaskRecord:
        """Create a task record in QUEUED state (no subprocess yet)."""
        task_id = str(uuid.uuid4())
        if log_file is None:
            paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = paths.LOG_DIR / f"{task_id}.log"
        else:
            log_file.parent.mkdir(parents=True, exist_ok=True)
        record = TaskRecord(
            task_id=task_id,
            task_type=task_type,
            description=description,
            status=TaskStatus.QUEUED,
            log_file=log_file,
            metadata=metadata or {},
            _on_finish=on_finish,
        )
        self._tasks[task_id] = record
        self._save()
        return record

    async def start_queued(
        self,
        record: TaskRecord,
        cmd: list[str],
        env: dict[str, str] | None = None,
        cwd: str | None = None,
    ) -> None:
        """Start the subprocess for a previously queued task."""
        merged_env = {**os.environ, **(env or {})}
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=merged_env,
            cwd=cwd,
        )
        record._process = process
        record.status = TaskStatus.RUNNING
        record.started_at = datetime.now(timezone.utc)
        self._save()
        asyncio.create_task(self._read_output(record))

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
        self._save()

        if record._on_finish:
            try:
                await record._on_finish(record)
            except Exception:
                pass

        return True


# Global singleton
task_manager = TaskManager()
