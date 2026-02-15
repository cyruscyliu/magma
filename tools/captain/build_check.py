#!/usr/bin/env python3
"""
Run the Magma build-check runner image (assumes the image is already built).

This script intentionally uses a single, stable image tag (default:
`magma/build-check:latest`) and selects behavior via `docker run --entrypoint`:
- target build-check: /usr/local/bin/magma_target_build_check
- fuzzer build-check: /usr/local/bin/magma_fuzzer_build_check

Back-compat environment variables (preferred by mmcp tooling):
- Target mode: TARGET, TARGET_VERSION (FUZZER is optional/ignored for tagging now)
- Fuzzer mode: FUZZER or FUZZER_NAME
- Common: MAGMA, CANARY_MODE, ISAN, HARDEN, SOURCE_COVERAGE
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_IMAGE = "magma/build-check:latest"


def _env_flag(name: str) -> bool:
    # Treat any non-empty value as enabled.
    return bool(os.environ.get(name, "").strip())


def _print_cmd(argv: list[str]) -> None:
    print("+ " + " ".join(argv), flush=True)


def _run(argv: list[str], *, check: bool = True) -> None:
    _print_cmd(argv)
    subprocess.run(argv, check=check)


def _default_magma_root() -> Path:
    # tools/captain/build_check.py -> tools/captain -> tools -> magma
    return Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--mode", choices=["target", "fuzzer"], default=os.environ.get("MODE", ""))
    ap.add_argument("--image", default=os.environ.get("IMG_NAME") or os.environ.get("IMAGE") or DEFAULT_IMAGE)
    ap.add_argument("--magma", default=os.environ.get("MAGMA", ""), help="Path to magma/ directory")

    ap.add_argument("--target", default=os.environ.get("TARGET", ""))
    ap.add_argument("--target-version", default=os.environ.get("TARGET_VERSION", ""))
    ap.add_argument("--canary-mode", type=int, default=int(os.environ.get("CANARY_MODE", "1") or "1"))
    ap.add_argument("--isan", action="store_true", default=_env_flag("ISAN"))
    ap.add_argument("--harden", action="store_true", default=_env_flag("HARDEN"))
    ap.add_argument("--source-coverage", action="store_true", default=_env_flag("SOURCE_COVERAGE"))

    ap.add_argument("--fuzzer", default=os.environ.get("FUZZER_NAME") or os.environ.get("FUZZER", ""))

    args = ap.parse_args()

    magma_root = Path(args.magma).expanduser().resolve() if args.magma else _default_magma_root()
    docker_dir = magma_root / "docker"

    # Infer mode if not explicitly set.
    mode = (args.mode or "").strip()
    if not mode:
        if args.target and args.target_version:
            mode = "target"
        elif args.fuzzer:
            mode = "fuzzer"
        else:
            print(
                "Must specify either target mode (TARGET + TARGET_VERSION) or fuzzer mode (FUZZER/FUZZER_NAME).",
                file=sys.stderr,
            )
            return 1

    if mode == "target":
        if not args.target or not args.target_version:
            print("TARGET and TARGET_VERSION must be set for target mode.", file=sys.stderr)
            return 1
        entrypoint = "/usr/local/bin/magma_target_build_check"
    else:
        if not args.fuzzer:
            print("FUZZER (or FUZZER_NAME) must be set for fuzzer mode.", file=sys.stderr)
            return 1
        entrypoint = "/usr/local/bin/magma_fuzzer_build_check"

    if args.canary_mode not in (1, 2, 3):
        print(f"Invalid CANARY_MODE: {args.canary_mode}. Must be 1, 2, or 3.", file=sys.stderr)
        return 1

    # Fail fast with a clearer error if the user forgot to build the image.
    _run(["docker", "image", "inspect", args.image], check=True)

    run_argv: list[str] = ["docker", "run", "--rm", "--entrypoint", entrypoint]

    if mode == "target":
        run_argv += ["-e", f"TARGET_NAME={args.target}"]
        run_argv += ["-e", f"TARGET_VERSION={args.target_version}"]
        run_argv += ["-e", f"CANARY_MODE={args.canary_mode}"]
        if args.isan:
            run_argv += ["-e", "ISAN=1"]
        if args.harden:
            run_argv += ["-e", "HARDEN=1"]
        if args.source_coverage:
            run_argv += ["-e", "SOURCE_COVERAGE=1"]

        run_argv += ["-v", f"{magma_root / 'magma'}:/magma/magma:ro"]
        run_argv += ["-v", f"{magma_root / 'targets'}:/magma/targets:rw"]
    else:
        run_argv += ["-e", f"FUZZER_NAME={args.fuzzer}"]
        run_argv += ["-v", f"{magma_root / 'magma'}:/magma/magma:ro"]
        # Fetch/build generally creates `${FUZZER}/repo`, so keep this RW.
        run_argv += ["-v", f"{magma_root / 'fuzzers'}:/magma/fuzzers:rw"]

    run_argv.append(args.image)
    _run(run_argv)

    # Keep status parsing consistent with build tasks: last line is the "image name".
    print(args.image, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
