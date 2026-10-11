---
name: magma
description: Build and run Magma fuzzing campaigns with Captain, inspect campaign results, collect source-based coverage, replay stored PoCs, and debug via a persistent REPL. Use for Magma fuzzer/target experiments and troubleshooting.
---

# Magma

Run commands from the repository root. Docker must be available; Magma's host dependencies are `util-linux`, `inotify-tools`, `docker.io`, and `git`.

## Quick Campaign

Use the names under `fuzzers/` and `targets/`; AFL++ is named `aflplusplus`.

```bash
FUZZER=aflplusplus TARGET=libpng tools/captain/build.sh

mkdir -p workdir/manual
FUZZER=aflplusplus TARGET=libpng PROGRAM=libpng_read_fuzzer \
  SHARED=workdir/manual POLL=5 TIMEOUT=10m tools/captain/start.sh
```

Find valid programs in `targets/<target>/configrc`. Use `tools/captain/run.sh <captainrc>` for repeated or parallel campaigns; start from `tools/captain/captainrc` and narrow `FUZZERS`, `<fuzzer>_TARGETS`, `REPEAT`, `WORKERS`, and `TIMEOUT`.

## Source Coverage

Coverage must be enabled while building the image:

```bash
FUZZER=aflplusplus TARGET=libpng SOURCE_COVERAGE=1 \
  tools/captain/build.sh
```

Run the campaign normally. After fuzzing, Magma replays the queue and writes these files under `SHARED`:

- `coverage_overtime.txt`
- `coverage-reports/`
- `coverage-reports.json`

Also inspect `findings/`, `monitor/`, and the Captain build/container logs. Treat a successful fuzz run without coverage files as a build/configuration failure; first confirm the image was built with `SOURCE_COVERAGE=1`.

## PoC Replay

Replays the stored PoCs (`targets/<target>/pocs/<BUG>.crash`) through their bound fuzzing harnesses and verifies each one triggers its bug via the Magma oracle (canaries). No campaign is run; the standard campaign image is reused.

```bash
FUZZER=aflplusplus tools/captain/run.sh workdir/poc.captainrc
```

In the captainrc set `POC_MODE=1`, `POC_TARGETS=(lua)`, and optionally `POC_FUZZER`. Per-bug harness bindings go in `tools/captain/poc/configs/<target>.conf` as `{BUG}_PROGRAM`; unbound PoCs are replayed through every program in `targets/<target>/configrc`. Output lines report `PoC <target>/<BUG> triggered <BUG> through harness <program>` and `No PoC stored for <target>/<BUG>`; the run exits non-zero if any PoC fails to trigger.

## Debug REPL

Build the image, then start a persistent container without launching a campaign:

```bash
mkdir -p workdir/debug
FUZZER=aflplusplus TARGET=libpng PROGRAM=libpng_read_fuzzer \
  SHARED=workdir/debug DEBUG_MODE=1 tools/captain/start.sh
source workdir/debug/debug.env
docker exec "$DEBUG_CONTAINER_NAME" /bin/bash -lc '<command>'
```

The repository is mounted read-write at `/workspace/magma`. Agents should prefer non-interactive `docker exec ... /bin/bash -lc`; humans can use `docker exec -it ... /bin/bash`. The container persists until `docker rm -f "$DEBUG_CONTAINER_NAME"`.

Official guide: https://hexhive.epfl.ch/magma/docs/getting-started.html
