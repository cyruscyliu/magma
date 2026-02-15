# Magma Knowledge Base

This document is a comprehensive reference for AI agents and developers working with the
Magma fuzzing benchmark. It explains every concept, directory, environment variable,
script, and workflow in the project.

---

## 1. What is Magma?

Magma is a **ground-truth fuzzing benchmark**. It embeds known bugs (with canary
instrumentation) into real-world C/C++ libraries, then runs different fuzzers against
them to measure how effectively each fuzzer finds and triggers those bugs.

Key properties:
- **Ground-truth**: Every bug is known in advance and instrumented with canaries
- **Reproducible**: All campaigns run inside Docker containers
- **Multi-fuzzer**: Supports 26+ different fuzzers
- **Multi-target**: 9 real-world library targets with 127 total bugs
- **Versioned**: Each target supports multiple release versions (PIONEER = latest, LEGACY_YYYY = year-pinned)

---

## 2. Top-Level Directory Structure

```
magma/
├── docker/              # Dockerfile for building campaign containers
├── fuzzers/             # 26+ fuzzer implementations (one directory each)
├── magma/               # Core Magma instrumentation library + campaign runtime
├── targets/             # 9 target library definitions + bug patches
├── tools/               # Orchestration (captain), analysis (benchd), reporting (report_df)
├── mmcp/           # MCP server for AI agent control
├── docs/                # BUILD.md and USAGE.md
├── gen_target_releases.py  # Script to manage target version definitions
└── README.md
```

---

## 3. Container Environment Variables

These environment variables are set inside every Magma Docker container and are
fundamental to understanding how scripts reference paths:

| Variable | Container Path | Purpose |
|----------|---------------|---------|
| `MAGMA_R` | `/magma` | Root of the Magma directory tree inside the container |
| `MAGMA` | `/magma/magma` | Path to core Magma support library (canary code, runtime scripts) |
| `OUT` | `/magma_out` | Where compiled binaries are stored (fuzzer-instrumented targets) |
| `COV` | `/magma_cov` | Where coverage-instrumented binaries are stored |
| `SHARED` | `/magma_shared` | Host-mounted volume for results, findings, monitor data |
| `FUZZER` | `/magma/fuzzers/{name}` | Path to the fuzzer's scripts and source |
| `TARGET` | `/magma/targets/{name}` | Path to the target's config, patches, corpus |
| `TARGET_NAME` | e.g. `libpng` | Human-readable name of the target |
| `TARGET_VERSION` | e.g. `PIONEER` | Which version/release of the target to use |
| `CC` | `/usr/bin/gcc` | C compiler (overridden by fuzzer's instrument.sh) |
| `CXX` | `/usr/bin/g++` | C++ compiler (overridden by fuzzer's instrument.sh) |

### Build-time flags injected via Docker build args:

| Build Arg | Resulting Define | Purpose |
|-----------|-----------------|---------|
| `canaries=1` | `-DMAGMA_ENABLE_CANARIES` | Compile canary logging macros into the target |
| `fixes=1` | `-DMAGMA_ENABLE_FIXES` | Compile the bug fixes (no bugs present) |
| `isan=1` | `-DMAGMA_FATAL_CANARIES` | Canary triggers cause SIGSEGV (like ASan) |
| `harden=1` | `-DMAGMA_HARDEN_CANARIES` | Protect canary storage with mprotect wrappers |
| `source_coverage=1` | `-fprofile-instr-generate -fcoverage-mapping` | LLVM source coverage |

### Runtime environment variables (set by captain scripts):

| Variable | Purpose |
|----------|---------|
| `PROGRAM` | Which binary to fuzz (e.g. `libpng_read_fuzzer`, `tiffcp`) |
| `ARGS` | Command-line arguments for the program (e.g. `-M @@ tmp.out` for tiffcp) |
| `FUZZARGS` | Extra arguments passed to the fuzzer itself |
| `POLL` | Seconds between canary monitor polls (default 5) |
| `TIMEOUT` | Campaign duration with suffix: `s`/`m`/`h`/`d` (e.g. `24h`) |
| `AFFINITY` | CPU core(s) to bind the container to (e.g. `0,1`) |

---

## 4. Output Directories Inside Containers

### `$OUT` = `/magma_out` — Compiled Artifacts

Contains the final fuzzer-instrumented binaries:
- `$OUT/{program}` — The instrumented binary (e.g. `$OUT/libpng_read_fuzzer`)
- `$OUT/magma.o` — Compiled canary + storage object linked into every target
- `$OUT/monitor` — The canary monitor binary
- `$OUT/afl/{program}` — AFL-specific instrumented binaries (some fuzzers)
- `$OUT/cmplog/{program}` — CMPLOG-instrumented binaries (AFL++)

### `$COV` = `/magma_cov` — Coverage Binaries

When `SOURCE_COVERAGE=1`, this directory contains LLVM coverage-instrumented
versions of the same binaries. Used by `magma/coverage.sh` to replay the corpus
and generate `.profraw` / `.profdata` files for coverage reports.

### `$SHARED` = `/magma_shared` — Results Volume

This is mounted from the host. During a campaign:
- `$SHARED/findings/` — Fuzzer crash/queue outputs (structure varies by fuzzer)
- `$SHARED/monitor/` — Time-series canary dumps (one file per poll, named by timestamp)
- `$SHARED/monitor/{timestamp}` — CSV with header: `BUG1_R,BUG1_T,BUG2_R,BUG2_T,...`
- `$SHARED/log/` — Fuzzer stdout/stderr (via `multilog`)
- `$SHARED/log/current` — Current log file
- `$SHARED/canaries.raw` — Shared memory file for live canary data (2048 bytes)
- `$SHARED/runonce.tmp` — Temporary file used by runonce.sh

---

## 5. Canary Instrumentation System

### What Canaries Are

Canaries are lightweight instrumentation points embedded in the target's source code
via patches. Each bug has a canary that detects two events:

1. **Reached**: The buggy code location was executed
2. **Triggered**: The bug condition was actually met (e.g., buffer overflow occurred)

### Canary Macros (defined in `magma/src/canary.h`)

```c
MAGMA_LOG(bug_name, condition)   // Log reach (always) + trigger (if condition is true)
MAGMA_LOG_V(bug_name, condition) // Same but returns the condition value
MAGMA_AND(a, b)                  // Inline assembly AND (avoids compiler optimization)
MAGMA_OR(a, b)                   // Inline assembly OR (avoids compiler optimization)
```

### How Canaries Work

1. `MAGMA_LOG("PNG001", overflow_detected)` calls `magma_log()` in `canary.c`
2. `magma_log()` writes to a shared memory region (`canaries.raw`, 2048 bytes)
3. The **monitor** binary reads this shared memory periodically and dumps CSV data
4. Each CSV row has columns: `{BUG}_R` (reached count) and `{BUG}_T` (triggered count)

### Shared Memory Layout (`storage.h`)

```
stored_data_t (2048 bytes total):
├── consumed: bool               # Flag for consumer synchronization
├── producer_buffer[BUFFERLEN]:   # Written by target process
│   └── canary_t:
│       ├── name[16]: char        # Bug name (e.g. "PNG001")
│       ├── reached: uint64       # Reach counter
│       └── triggered: uint64     # Trigger counter
└── consumer_buffer[BUFFERLEN]:   # Read by monitor process
    └── canary_t: (same structure)
```

BUFFERLEN ≈ 60 entries (depending on alignment), meaning up to ~60 distinct bugs
can be tracked per target.

### Monitor Binary (`magma/src/monitor.c`)

```bash
# Dump canary data from shared memory file
$OUT/monitor --dump raw     # Binary dump
$OUT/monitor --dump row     # CSV header + data row
$OUT/monitor --dump human   # Human-readable table

# Watch mode: execute a command, then read shared memory
$OUT/monitor --fetch watch --dump human "$FUZZER/runonce.sh" "$testcase"

# File mode: read from shared memory file
$OUT/monitor --fetch file --dump row "$SHARED/canaries.raw"
```

### Canary Modes (CANARY_MODE in captainrc)

| Mode | `canaries` | `fixes` | Effect |
|------|-----------|---------|--------|
| 1 | yes | no | Bugs present + canary logging enabled (standard benchmarking) |
| 2 | no | no | Bugs present, no canaries (testing fuzzer without instrumentation overhead) |
| 3 | no | yes | Bugs fixed, no canaries (baseline/control) |

---

## 6. Targets

### Target Directory Structure

```
targets/{target_name}/
├── configrc              # PROGRAMS array + per-program ARGS
├── releases              # Version definitions (git URLs + tags/commits)
├── preinstall.sh         # apt-get install build dependencies
├── build.sh              # Build the library + fuzzer targets
├── build_poc.sh          # Build clean version for PoC reproduction
├── patches/
│   ├── setup/            # Build system integration patches
│   │   └── *.patch       # Applied first: make the library build with Magma
│   └── bugs/             # Bug injection patches
│       └── {BUGID}.patch # Each patch injects one bug with canary macros
├── corpus/
│   └── {program}/        # Seed input files for each program
│       └── seed_*        # Actual seed files (PNG files, TIFF files, etc.)
├── pocs/                 # Known proof-of-concept crash inputs
│   └── {BUGID}.crash     # One crash file per known-triggered bug
└── src/                  # Target-specific source files (optional)
```

### Available Targets

| Target | Programs | Bug Count | Description |
|--------|----------|-----------|-------------|
| libpng | `libpng_read_fuzzer` | 7 (PNG001-PNG007) | PNG image library |
| libsndfile | `sndfile_fuzzer` | 18 (SND001-SND018) | Audio file I/O library |
| libtiff | `tiff_read_rgba_fuzzer`, `tiffcp` | 14 (TIF001-TIF014) | TIFF image library |
| libxml2 | `libxml2_xml_read_memory_fuzzer`, `xmllint` | 8 (XML001-XML008) | XML parser |
| lua | `lua_driver` | 4 (LUA001-LUA004) | Lua scripting interpreter |
| openssl | 6 programs (asn1, bignum, client, server, x509) | 20 (SSL001-SSL020) | TLS/crypto library |
| php | 4 programs (json, parser, exif, unserialize) | 16 (PHP001-PHP016) | PHP interpreter |
| poppler | 3 programs (pdf_fuzzer, pdftoppm, pdfimages) | 22 (PDF001-PDF022) | PDF rendering |
| sqlite3 | `sqlite3_fuzz` | 18 (SQL001-SQL018) | SQLite database engine |

### configrc Format

```bash
PROGRAMS=(libpng_read_fuzzer)         # Array of program names
# Per-program arguments (optional):
tiffcp_ARGS="-M @@ tmp.out"          # @@ = input file placeholder
xmllint_ARGS="--valid --oldxml10 --push --memory @@"
sndfile_fuzzer_ARGS="@@"
```

### releases Format

```bash
libpng_PIONEER="https://github.com/pnggroup/libpng.git"
libpng_PIONEER_STABLE_COMMIT="abc123..."
libpng_LEGACY_2024="https://github.com/pnggroup/libpng.git"
libpng_LEGACY_2024_TAG="v1.6.44"
```

- `PIONEER` = latest development version (pinned by commit hash)
- `LEGACY_YYYY` = version released in year YYYY (pinned by tag)

### Bug Patch Format

Each `.patch` file uses `%MAGMA_BUG%` as a placeholder that gets substituted with
the bug name (e.g., `PNG001`) during `apply_patches.sh`:

```c
#ifdef MAGMA_ENABLE_FIXES
    // Fixed version of the code
    size_t row_factor = checked_multiply(height, width);
#else
    // Buggy version
    size_t row_factor = (png_uint_32)(height * width);  // overflow!
  #ifdef MAGMA_ENABLE_CANARIES
    MAGMA_LOG("%MAGMA_BUG%", height * width != row_factor);
  #endif
#endif
```

---

## 7. Fuzzers

### Fuzzer Directory Structure

```
fuzzers/{fuzzer_name}/
├── preinstall.sh     # apt-get install fuzzer build dependencies
├── fetch.sh          # Clone/download the fuzzer source code
├── build.sh          # Compile the fuzzer
├── instrument.sh     # Set CC/CXX to fuzzer's compiler wrappers
├── run.sh            # Execute a full fuzzing campaign
├── runonce.sh        # Execute a single test case
├── findings.sh       # List crash file paths from fuzzer output
├── coverage.sh       # Coverage collection configuration (optional)
├── postinstall.sh    # Post-build setup (optional)
└── src/              # Fuzzer-specific source code (optional)
```

### Key Fuzzer Scripts

**instrument.sh** — Sets compiler environment for target instrumentation:
```bash
# Example: AFL++ sets these so the target gets compiled with AFL instrumentation
export CC="$FUZZER/repo/afl-clang-fast"
export CXX="$FUZZER/repo/afl-clang-fast++"
export AS="llvm-as"
```

**run.sh** — Launches the fuzzer (called by `$MAGMA/run.sh` inside the container):
```bash
$FUZZER/repo/afl-fuzz -i "$TARGET/corpus/$PROGRAM" \
    -o "$SHARED/findings" \
    $FUZZARGS -- "$OUT/afl/$PROGRAM" $ARGS
```

**runonce.sh** — Runs a single input (used by extract.sh and test validation):
```bash
timeout -s SIGKILL ${TIMELIMIT:-0.1} \
    "$OUT/$PROGRAM" ${ARGS/@@/$1}
```

**findings.sh** — Lists crash files:
```bash
find "$SHARED/findings/default/crashes" -type f -name 'id:*'
```

### Available Fuzzers (26)

AFL family: `afl`, `afl_asan`, `afl_resume`, `aflfast`, `aflplusplus`, `aflplusplus_lto`, `aflplusplus_lto_asan`
Honggfuzz: `honggfuzz`, `honggfuzz_asan`
Specialized: `angora`, `ddfuzz`, `eclipser`, `entropic`, `fairfuzz`, `instrim`, `k_scheduler`, `libfuzzer`, `moptafl`, `moptafl_asan`, `parmesan`
Symbolic: `klee`, `symcc_afl`, `symcc_analysis`
Utilities: `llvm_analysis`, `llvm_cov`, `vanilla`

---

## 8. Orchestration (tools/captain/)

### captainrc Configuration

```bash
WORKDIR=./workdir         # Results directory
REPEAT=3                  # Campaigns per fuzzer/target/program
TIMEOUT=24h               # Duration per campaign
POLL=5                    # Monitor poll interval (seconds)
CANARY_MODE=1             # 1=canaries, 2=nothing, 3=fixes
TARGET_VERSION=PIONEER    # Which version to test
CAMPAIGN_WORKERS=1        # CPUs per campaign
FUZZERS=(afl aflfast aflplusplus honggfuzz)  # Which fuzzers to evaluate

# Per-fuzzer overrides:
# afl_TARGETS=(libpng libtiff)           # Restrict targets for a fuzzer
# afl_libpng_PROGRAMS=(libpng_read_fuzzer)  # Restrict programs
# afl_libpng_FUZZARGS="-x dict.txt"      # Extra fuzzer args
# afl_CAMPAIGN_WORKERS=3                  # Override CPU count
```

### Captain Scripts

| Script | Purpose | Key Env Vars |
|--------|---------|-------------|
| `build.sh` | Build Docker image for fuzzer/target | `FUZZER`, `TARGET`, `TARGET_VERSION`, `CANARY_MODE`, `ISAN`, `HARDEN`, `SOURCE_COVERAGE` |
| `run.sh` | Orchestrate full experiment (all fuzzers x targets x repeats) | Reads `captainrc` |
| `start.sh` | Launch single Docker campaign container | `FUZZER`, `TARGET`, `PROGRAM`, `ARGS`, `FUZZARGS`, `POLL`, `TIMEOUT`, `SHARED`, `AFFINITY` |
| `extract.sh` | Extract PoCs from campaign findings | `FUZZER`, `TARGET`, `PROGRAM`, `ARGS`, `SHARED`, `POCDIR` |
| `post_extract.sh` | Bulk extraction from archived results | `WORKDIR` |
| `common.sh` | Shared utilities (sourced by other scripts) | `MAGMA` |

### common.sh Utilities

- `echo_time(msg)` — Timestamped logging: `[2024-01-15 14:30] msg`
- `contains_element(needle, array...)` — Array membership check
- `get_var_or_default(prefix, key1, key2, ...)` — Hierarchical variable resolution:
  tries `{prefix}_{key1}_{key2}`, then `DEFAULT_{key1}_{key2}`, then `{key1}_{key2}`
- Auto-loads all target configrc files into `DEFAULT_{target}_PROGRAMS` arrays

### Docker Container Launch (start.sh)

```bash
docker run -dt \
    --volume=$SHARED:/magma_shared \       # Mount results volume
    --cap-add=SYS_PTRACE \                 # For debugging/ASan
    --security-opt seccomp=unconfined \     # Full syscall access
    --env=PROGRAM="$PROGRAM" \
    --env=ARGS="$ARGS" \
    --env=FUZZARGS="$FUZZARGS" \
    --env=POLL="$POLL" \
    --env=TIMEOUT="$TIMEOUT" \
    --network=none \                        # Network isolation
    --cpuset-cpus=$AFFINITY \              # CPU binding
    "magma/$FUZZER/$TARGET"
```

---

## 9. Campaign Workflow (End-to-End)

### Phase 1: Build
```
captain/build.sh
└── docker build -t "magma/$FUZZER/$TARGET"
    └── Dockerfile stages:
        1. Ubuntu 24.04 base + magma user
        2. Copy magma/ → compile canary library (canary.o + storage.o → magma.o)
        3. Copy fuzzer → fetch source, compile fuzzer
        4. Copy target → fetch target source via git, apply patches
        5. Run fuzzer/instrument.sh (set CC/CXX to fuzzer's compiler)
        6. Target build.sh compiles library with fuzzer instrumentation
        7. ENTRYPOINT → $MAGMA/run.sh
```

### Phase 2: Launch Campaign
```
captain/start.sh → docker run container
└── Container entrypoint: magma/run.sh
    ├── Prune seed corpus (remove fault-triggering seeds)
    ├── Start monitor loop (background):
    │   └── Every $POLL seconds: dump canary data → $SHARED/monitor/{timestamp}
    ├── Start fuzzer: timeout $TIMEOUT $FUZZER/run.sh
    │   └── Fuzzer writes crashes to $SHARED/findings/
    └── On timeout: kill fuzzer + monitor, optionally run coverage.sh
```

### Phase 3: Collect Results
```
Campaign workdir structure:
$WORKDIR/
├── ar/{fuzzer}/{target}/{program}/{run_id}/
│   └── ball.tar           # Archived campaign data (monitor/ + findings/)
├── cache/{fuzzer}/{target}/{program}/{run_id}/
│   └── (live shared volume during campaign, moved to ar/ after)
├── log/
│   ├── {fuzzer}_{target}_{program}_{run}_container.log
│   └── monitor/           # (older format)
└── poc/
    └── {fuzzer}_{target}_{program}_{BUGID}.XXX  # Extracted PoCs
```

### Phase 4: Extract PoCs
```
captain/extract.sh
├── List crashes via $FUZZER/findings.sh
├── For each crash:
│   ├── Run magma/runonce.sh inside container
│   ├── Monitor detects canary trigger
│   ├── Parse "exit_code N bug BUGID"
│   └── Copy crash file to $POCDIR/{fuzzer}_{target}_{program}_{BUGID}.XXX
└── Filter: only keep crashes that trigger known bugs
```

### Phase 5: Analyze Results
```
tools/benchd/exp2json.py workdir results.json
├── Walk workdir/ar/{fuzzer}/{target}/{program}/{run}/
├── Extract monitor/ from ball.tar
├── Parse CSV rows: timestamp → {BUG_R, BUG_T} counters
├── Compute time-to-bug (first timestamp where counter > 0)
└── Output JSON: {results: {fuzzer: {target: {program: {run: {reached: {}, triggered: {}}}}}}}
```

### Phase 6: Generate Reports
```
tools/report_df/main.py results.json output_dir/
├── Load JSON experiment data
├── Compute survival curves (time-to-first-trigger)
├── Generate comparison tables (fuzzer × bug)
├── Create Matplotlib/Seaborn plots
└── Render HTML report via Jinja2 templates
```

---

## 10. Monitor Data Format

Each file in `$SHARED/monitor/` is a CSV with one header line and one data line:

```csv
PNG001_R,PNG001_T,PNG002_R,PNG002_T,...,PNG007_R,PNG007_T
5230,12,0,0,...,841,0
```

- `{BUG}_R` = Reached counter (how many times the buggy code was executed)
- `{BUG}_T` = Triggered counter (how many times the bug condition was true)
- Filename = integer timestamp (seconds since campaign start, in $POLL increments)

---

## 11. runonce.sh — Single Input Testing

`magma/runonce.sh` is the key script for validating whether a test case triggers a bug:

```
Input: test case file path
Process:
  1. Copy file to $SHARED/runonce.tmp
  2. Run: $OUT/monitor --fetch watch --dump human "$FUZZER/runonce.sh" "$SHARED/runonce.tmp"
  3. Monitor reads canary shared memory after execution
  4. Parse output for any triggered canary (reached + triggered > 0)
Output: "exit_code N bug BUGID" or "exit_code N" (if no bug triggered)
Exit code: 0 = no bug, non-zero = bug triggered or crash
```

---

## 12. MCP Server (`mmcp/`)

The MCP (Model Context Protocol) server allows AI agents to control Magma programmatically.

### Running the Server

```bash
# Install dependencies
pip install -r mmcp/requirements.txt

# Run via Python module
cd /path/to/magma
python -m mmcp

# Or configure in Claude/MCP client:
{
  "mcpServers": {
    "magma": {
      "command": "python",
      "args": ["-m", "mmcp"],
      "cwd": "/path/to/magma"
    }
  }
}
```

### Available Tools (11)

**Build**:
`magma_build_image`, `magma_build_images`, `magma_get_task_log`, `magma_list_images`

**Campaign**:
`magma_start_campaign`, `magma_stop_campaign`, `magma_get_campaign_status`,
`magma_list_campaigns`, `magma_configure_cpus`, `magma_cpu_status`

**Results**:
`magma_get_campaign_results`

### Available Resources (12 URIs)

`magma://targets`, `magma://targets/{t}`, `magma://targets/{t}/configrc`,
`magma://targets/{t}/releases`, `magma://targets/{t}/bugs`,
`magma://targets/{t}/bugs/{id}`, `magma://targets/{t}/corpus/{p}`,
`magma://fuzzers`, `magma://fuzzers/{f}`, `magma://fuzzers/{f}/{script}`,
`magma://config/captainrc`, `magma://docker/images`

### Async Operations

Long-running operations (build, campaign) return a `task_id`.
Poll with `magma_get_campaign_status(batch_id, task_ids)` to check progress. Use
`magma_stop_campaign(batch_id, task_ids)` to cancel.

---

## 13. Docker Image Naming Convention

```
magma/{fuzzer}/{target}          # Standard campaign image
magma/{target}/{bug_id}          # PoC reproduction image (magma_pocs stage)
```

Build with `CANARY_MODE` controls what gets compiled:
- Mode 1: `--build-arg canaries=1` → bugs + canary logging
- Mode 2: (no args) → bugs only, no canaries
- Mode 3: `--build-arg fixes=1` → bugs fixed

---

## 14. File-Level Quick Reference

| File | What It Does |
|------|-------------|
| `docker/Dockerfile` | Multi-stage build: `magma_core` (campaigns) + `magma_pocs` (reproduction) |
| `magma/preinstall.sh` | Install multilog (daemontools) for log rotation |
| `magma/prebuild.sh` | Compile monitor binary from C source |
| `magma/build.sh` | Compile canary.o + storage.o → magma.o linked into targets |
| `magma/run.sh` | Campaign entrypoint: prune seeds, start monitor loop, start fuzzer |
| `magma/runonce.sh` | Single test case validation via monitor |
| `magma/fetch_target.sh` | Git clone or wget the target source using releases file |
| `magma/apply_patches.sh` | Apply setup/ + bugs/ patches, substitute `%MAGMA_BUG%` |
| `magma/coverage.sh` | Replay corpus for LLVM source coverage collection |
| `magma/src/canary.{c,h}` | Canary logging implementation + macros |
| `magma/src/storage.{c,h}` | Shared memory storage for canary data |
| `magma/src/monitor.c` | Monitor binary: reads shared memory, dumps CSV/human output |
| `magma/src/source_coverage.c` | Hooks for LLVM coverage instrumentation |
| `tools/captain/captainrc` | Campaign configuration template |
| `tools/captain/build.sh` | Build Docker image from Dockerfile |
| `tools/captain/run.sh` | Full experiment orchestrator |
| `tools/captain/start.sh` | Launch single campaign container |
| `tools/captain/extract.sh` | Extract PoCs from findings |
| `tools/captain/common.sh` | Shared utilities + config auto-loading |
| `tools/benchd/exp2json.py` | workdir → JSON results (time-to-bug data) |
| `tools/benchd/survival_analysis.py` | Statistical analysis of bug discovery |
| `tools/report_df/main.py` | JSON → HTML report with plots |
