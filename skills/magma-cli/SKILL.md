---
name: magma-cli
description: Build Magma fuzzer/target Docker images, run fuzzing campaigns, and replay inputs through the bug oracle using the repository-root magma-cli. Use for agent-driven CLI experiments, configuration discovery, dry runs, and interpreting JSON results or failures.
---

# Magma CLI

Run `./magma-cli` from the repository root, or invoke it by absolute path from
another directory. It requires Python 3.9+ and Bash; build, run and replay also
require Docker. No Python packages or running MCP server are needed.

## Discover the available configuration

```bash
./magma-cli --help
./magma-cli list fuzzers
./magma-cli list targets
./magma-cli list programs --target libpng
./magma-cli list versions --target libpng
./magma-cli list bugs --target libpng
```

`list targets` includes each target's programs and versions. Archived fuzzers
under `fuzzers/graveyard/` are excluded. Programs and their default arguments
come from the checkout's `targets/<target>/configrc`.

## Build

```bash
./magma-cli build --fuzzer aflplusplus --target libpng
```

The default target version is `FIXED`: source is selected by the original
`targets/<target>/fetch.sh`. For this example the default image is
`magma-cli/v1.2-next/aflplusplus/libpng:fixed`. `--target-version default` and
`--target-version FIXED` select this snapshot; other versions fail before calling
Docker. Generated releases metadata does not change the fixed fetch behavior.
Builds use the caller's UID/GID (1000 when invoked as root).

Options include `--canary-mode canaries|plain|fixes`, `--isan`, `--harden`,
`--source-coverage`, `--no-cache`, `--image NAME` and `--log-file PATH`.
Canaries are enabled by default. The same default image tag is reused when
changing build options; use separate `--image` names to keep several modes.

`--source-coverage` requires a fuzzer with `coverage.sh`. Coverage-enabled images
collect the existing source coverage reports after a campaign. Coverage support
and artifacts otherwise follow this checkout's scripts.

## Run a campaign

```bash
./magma-cli run \
  --fuzzer aflplusplus --target libpng --program libpng_read_fuzzer \
  --workdir workdir/example --timeout 10m --poll 5
```

Build the image first. `run` waits in the foreground and writes findings, monitor
samples, fuzzer logs and `cli.log` into `--workdir`. The directory must be new or
empty. A campaign reaching its timeout completes successfully; a fuzzer failure
returns a failure exit code. The timeout covers fuzzing; seed validation and
optional coverage collection can add time.

Use `--affinity 0,2-3` to choose CPUs, `--fuzz-args='-m none'` for fuzzer arguments,
and `--args='-M @@ output.tif'` to override program arguments. Omitted `--args`
uses `configrc`; `--args=''` explicitly selects an empty argument string.
Options whose values begin with a dash should use the `--option=value` form.

The container runs with the caller's UID/GID and no network access. SIGINT or
SIGTERM stops the CLI and removes its container; output files remain available.
Each invocation runs one campaign. Launch multiple CLI processes with distinct
workdirs and, when needed, nonoverlapping CPU affinities for parallel trials.

## Replay inputs

```bash
./magma-cli replay \
  --fuzzer aflplusplus --target libpng --program libpng_read_fuzzer \
  --input targets/libpng/corpus/libpng_read_fuzzer/not_kitty_gamma.png

./magma-cli replay \
  --fuzzer aflplusplus --target libpng --program libpng_read_fuzzer \
  --input /path/to/testcase --expect-bug PNG002
```

`--input` accepts a file or a directory searched recursively, and may be repeated.
Duplicate files are replayed once. Each file is mounted read-only and copied to
an isolated writable directory in a fresh container. `--timeout 10s` limits each
replay including container startup; the selected fuzzer wrapper also imposes its
own per-input time/memory limits.

Each result includes `input`, `status`, `process_exit_code`, `triggered_bugs` and
`bugs` (the oracle's reached/triggered counts). Status is `clean`, `triggered`,
`failed`, `timeout` or `expectation_failed`. All oracle bug rows are retained.
`process_exit_code` comes from the existing monitor/fuzzer wrapper, which may
normalize target crashes; it is not necessarily the target's raw exit status.

A confirmed oracle trigger is a successful replay even if the wrapper exits 1.
`--expect-bug` requires every input to trigger the named bug, and requires an
image built with canaries. Inputs without a trigger can otherwise be successful
replays. This command consumes supplied files; it does not generate or migrate
stored PoCs.

## Automation contract

Every completed command writes one JSON object to stdout, including failures.
`--help` and `--version` print text. JSON contains `schema_version: 1`, `release`,
`command`, `status` and `exit_code`, plus command-specific fields. Subprocess logs
go to stderr; use `--log-file` to also save them. Existing log files are never
replaced. For replay, the saved log includes target diagnostics and oracle rows.

| Exit code | Meaning |
| --- | --- |
| `0` | Successful operation or dry run, including confirmed replay triggers |
| `1` | Build, runtime, Docker, I/O or replay timeout failure |
| `2` | Invalid arguments, configuration, input or unsupported version |
| `3` | Replay completed but at least one input missed `--expect-bug` |
| `130` | Interrupted by SIGINT or SIGTERM |

Build/run failures also report the underlying `process_exit_code`. Replay reports
that code per input. Batch replay continues after individual failures and returns
`1` if any operational failure occurred, otherwise `3` for unmet expectations.

Add `--dry-run` to build, run or replay to get an argument-array plan without
Docker calls, image inspection or filesystem writes:

```bash
./magma-cli build --fuzzer aflplusplus --target libpng --dry-run
./magma-cli run --fuzzer aflplusplus --target libpng \
  --program libpng_read_fuzzer --workdir workdir/planned --dry-run
```

`--image NAME` works consistently on all three commands and can select an
existing Captain image. The CLI checks the image's fuzzer/target environment and
CLI version labels when present. Older unlabeled images cannot be checked for
release/snapshot identity; select those explicitly with care.

For agents, first inspect `list` output, then optionally inspect a dry run, build,
run into a fresh workdir and replay interesting findings. Keep stdout as JSON and
stderr as diagnostic logs. `MAGMA` in the caller's environment does not redirect
the CLI to another checkout.
