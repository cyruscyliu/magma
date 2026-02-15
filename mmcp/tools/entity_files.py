"""Generic file tools for Magma entities (targets/fuzzers)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

from mcp.server.fastmcp import FastMCP

from ..core import paths


def _entity_root(entity_type: str, entity_name: str) -> Path:
    et = entity_type.strip().lower()
    if et == "target":
        root = paths.TARGETS_DIR / entity_name
    elif et == "fuzzer":
        root = paths.FUZZERS_DIR / entity_name
    elif et == "magma":
        # Magma support scripts live under magma/magma.
        # entity_name is ignored but kept in the API for consistency.
        root = paths.MAGMA_LIB_DIR
    else:
        raise ValueError(f"Invalid entity_type: {entity_type}")
    if not root.is_dir():
        raise ValueError(f"{et} not found: {entity_name}")
    return root


def _safe_entity_file(root: Path, relpath: str) -> Path:
    if not relpath or relpath.startswith("/"):
        raise ValueError("relpath must be a non-empty relative path")
    p = (root / relpath).resolve()
    if root.resolve() not in p.parents and p != root.resolve():
        raise ValueError("relpath escapes entity root")
    return p


def _validate_glob(glob_pattern: str) -> str:
    gp = (glob_pattern or "").strip()
    if not gp:
        raise ValueError("glob must be a non-empty relative glob pattern")
    if gp.startswith("/"):
        raise ValueError("glob must be relative (must not start with '/')")
    # Prevent `../` escapes via glob patterns.
    if ".." in Path(gp).parts:
        raise ValueError("glob must not contain '..'")
    return gp


def _iter_files(root: Path, glob_pattern: str) -> Iterable[Path]:
    # Path.glob supports `**` patterns and stays within the root as long as
    # we disallow `..` above.
    yield from root.glob(glob_pattern)


def _backup_path_for(file_path: Path) -> Path:
    backup_dir = file_path.parent / ".mmcp_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    return backup_dir / f"{file_path.name}.{ts}.bak"


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_list_entity_files(
        entity_type: str,
        entity_name: str,
        glob: str = "**/*",
        max_results: int = 2000,
    ) -> str:
        """List files under a target/fuzzer/magma entity directory.

        Args:
            entity_type: 'target', 'fuzzer', or 'magma'
            entity_name: entity directory name (ignored for entity_type='magma')
            glob: relative glob pattern (default '**/*')
            max_results: cap to avoid huge responses (default 2000)
        """
        try:
            root = _entity_root(entity_type, entity_name)
            gp = _validate_glob(glob)

            max_results = int(max_results)
            if max_results <= 0:
                return json.dumps({"error": "max_results must be > 0"})

            files: list[str] = []
            truncated = False

            for p in _iter_files(root, gp):
                # Skip directories and anything that resolves outside root.
                if not p.is_file():
                    continue
                rp = p.resolve()
                if root.resolve() not in rp.parents and rp != root.resolve():
                    continue
                rel = str(rp.relative_to(root.resolve()))
                files.append(rel)
                if len(files) >= max_results:
                    truncated = True
                    break

            files = sorted(set(files))

            return json.dumps(
                {
                    "entity_type": entity_type,
                    "entity_name": entity_name,
                    "glob": gp,
                    "count": len(files),
                    "truncated": truncated,
                    "files": files,
                },
                indent=2,
            )
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    async def magma_read_entity_file(
        entity_type: str,
        entity_name: str,
        relpath: str,
    ) -> str:
        """Read file content from a target or fuzzer directory."""
        try:
            root = _entity_root(entity_type, entity_name)
            path = _safe_entity_file(root, relpath)
            if not path.is_file():
                return json.dumps({"error": f"File not found: {path}"})
            return json.dumps(
                {
                    "entity_type": entity_type,
                    "entity_name": entity_name,
                    "relpath": relpath,
                    "path": str(path),
                    "content": path.read_text(),
                },
                indent=2,
            )
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    async def magma_update_entity_file(
        entity_type: str,
        entity_name: str,
        relpath: str,
        content: str,
        backup: bool = True,
    ) -> str:
        """Overwrite file content for target/fuzzer file, optionally backing up."""
        try:
            root = _entity_root(entity_type, entity_name)
            path = _safe_entity_file(root, relpath)
            backup_path = None
            if backup and path.exists():
                b = _backup_path_for(path)
                b.write_text(path.read_text())
                backup_path = str(b)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return json.dumps(
                {
                    "entity_type": entity_type,
                    "entity_name": entity_name,
                    "relpath": relpath,
                    "path": str(path),
                    "backup_path": backup_path,
                },
                indent=2,
            )
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    async def magma_restore_entity_file(
        entity_type: str,
        entity_name: str,
        relpath: str,
        backup_path: str,
    ) -> str:
        """Restore file content from a backup created by magma_update_entity_file."""
        try:
            root = _entity_root(entity_type, entity_name)
            path = _safe_entity_file(root, relpath)
            src = Path(backup_path).resolve()
            if not src.is_file():
                return json.dumps({"error": f"Backup not found: {backup_path}"})
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(src.read_text())
            return json.dumps(
                {
                    "entity_type": entity_type,
                    "entity_name": entity_name,
                    "relpath": relpath,
                    "path": str(path),
                    "restored_from": str(src),
                },
                indent=2,
            )
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    async def magma_patch_entity_file(
        entity_type: str,
        entity_name: str,
        relpath: str,
        patch_text: str,
        backup: bool = True,
    ) -> str:
        """Patch file by simple text replacement rules.

        patch_text format:
        JSON string with {"replace": [{"from": "...", "to": "..."}]}
        """
        try:
            root = _entity_root(entity_type, entity_name)
            path = _safe_entity_file(root, relpath)
            if not path.is_file():
                return json.dumps({"error": f"File not found: {path}"})
            try:
                spec = json.loads(patch_text)
            except json.JSONDecodeError:
                return json.dumps({"error": "patch_text must be valid JSON"})
            rules = spec.get("replace", []) if isinstance(spec, dict) else []
            if not isinstance(rules, list):
                return json.dumps({"error": "patch_text.replace must be a list"})

            original = path.read_text()
            updated = original
            applied = 0
            for item in rules:
                if not isinstance(item, dict):
                    continue
                src = item.get("from")
                dst = item.get("to", "")
                if not isinstance(src, str) or not isinstance(dst, str):
                    continue
                if src in updated:
                    updated = updated.replace(src, dst)
                    applied += 1

            backup_path = None
            if backup:
                b = _backup_path_for(path)
                b.write_text(original)
                backup_path = str(b)
            path.write_text(updated)
            return json.dumps(
                {
                    "entity_type": entity_type,
                    "entity_name": entity_name,
                    "relpath": relpath,
                    "path": str(path),
                    "backup_path": backup_path,
                    "rules_applied": applied,
                },
                indent=2,
            )
        except Exception as exc:
            return json.dumps({"error": str(exc)})
