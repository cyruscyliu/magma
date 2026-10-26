# SUMMARY: local branches vs upstream [HexHive/magma](https://github.com/HexHive/magma)

Both local branches are strict descendants of HexHive's `v1.2`
(`75d1ae7b`, "Merge pull request #129 from HexHive/dev"); neither is
behind upstream.

- **Part I** — `v1.2-next` (worktree `v1-2-1`) vs `hexhive/v1.2`
- **Part II** — `v1.4` (worktree `v1-4`) vs `hexhive/v1.2`

The two branches share the agent-facing tooling (MCP server, CLI,
skills, PoC mode, debug mode, coverage pipeline, report fixes) but
differ in how far the *benchmark itself* was modernized: `v1.2-next`
keeps the original v1.2-era targets on Ubuntu 18.04, while `v1.4`
carries the 2026 target/fuzzer migration on Ubuntu 24.04 with a
release/version system.

---

# Part I — `v1.2-next` vs `hexhive/v1.2`

## Relationship

| | |
|---|---|
| `hexhive/v1.2` HEAD | `75d1ae7b` |
| Behind HexHive | **0 commits** — strict descendant |
| Ahead of HexHive | 66 commits |
| Tree delta | 104 files, **+7,703 / −111** lines |

`v1.2-next` preserves HexHive v1.2 as-is (same Ubuntu 18.04 base image,
same 26 fuzzers, same 9 targets and bug-patch sets, same `fetch.sh`
mechanism) and only **adds** functionality on top. Everything below is
additive unless noted.

### 1. MCP server (`mmcp/`, ~4,300 lines)

`python -m mmcp` — Model Context Protocol server for agent-driven
operation (absent upstream):

- `mmcp/core/`: captainrc `config_parser`, `cpu_allocator` (CPU
  assignment across campaigns), `docker_utils`, `paths`, disk-persisted
  `task_manager` (UUID batch IDs, user-assigned IDs, task logs).
- `mmcp/tools/`: `build` (single/matrix images),
  `campaign` (start/stop/status/queue), `results` (extraction, PoC
  analysis, `magma_run_testcase`), `entity_files` (file listing).
- `mmcp/resources/`: `magma://targets`, `magma://fuzzers`,
  `magma://config/captainrc`, `magma://docker/images`, etc.
- `mmcp/tests/`: 9 test files (server, campaign, results, paths,
  allocator, entity files, config parser).

### 2. Repository CLI (`magma-cli` + `tools/cli/`, ~1,400 lines)

- Subcommands: `list` (fuzzers/targets/programs), `build`, `run`
  (single campaign **and** `--config <captainrc>` full Captain runs),
  `replay` (single file/dir, `--expect-bug` validation), `report`
  (Captain workdir → `benchd/exp2json` → `report_df` → static HTML).
- JSON results on stdout, logs on stderr, `--dry-run`, log files,
  container cleanup on interrupt; exit codes distinguish build/run/
  replay failures.
- Agent docs in `skills/magma-cli/SKILL.md` (+ `skills/magma/`).

### 3. Source-coverage pipeline

- `magma/coverage.sh` (+47), `magma/coverage_overtime.py` (+148),
  `magma/src/source_coverage.c` (+33), `magma/prebuild.sh`.
- Per-fuzzer `coverage.sh` / `instrument.sh` / `runonce.sh` support for
  aflplusplus, honggfuzz, libfuzzer.
- `magma/apply_patches.sh` (+8): applies the setup patches to the
  `$COV/repo` checkout when `SOURCE_COVERAGE` is set.
- `tools/report_df/CoverageData.py` (+373): coverage-over-time data,
  `coverage_template.md`, cov report linked into the main report,
  `tools/report_df/README.md`.

### 4. PoC mode

- `POC_MODE=1` in a captainrc switches `tools/captain/run.sh` from
  fuzzing campaigns to **PoC replay**: each stored PoC
  (`targets/<t>/pocs/<BUG>.crash`) is re-run through its bound fuzzing
  harness, built with the Magma canary oracle, to verify it reliably
  triggers its bug; no campaigns are run.
- `POC_TARGETS` selects the targets; `POC_FUZZER` picks the fuzzer used
  to build the PoC images (default: first `FUZZERS` entry); per-bug
  harness bindings live in `tools/captain/poc/configs/<TARGET>.conf`.
- Current slice on this branch: `tools/captain/poc/run.sh` (+105) +
  `configs/lua.conf` + `targets/lua/pocs/LUA004.crash` (Lua only).
- Upstream v1.2 has no PoC system at all (0 `pocs/` files, no
  `build_poc.sh`, no `magma_pocs` stage) — the full PoC build/run
  system exists only in the cyruscyliu fork's later work, not in
  HexHive.

### 5. Debug mode

- `DEBUG_MODE=1` (alias `MAGMA_DEBUG`) turns a Captain run into a
  **persistent inspection container** instead of a campaign:
  `tools/captain/run.sh` forces `CACHE_ON_DISK=1`, `NO_ARCHIVE=1`,
  `REPEAT=1` and limits the run to the first fuzzer/target;
  `tools/captain/start.sh` starts a long-lived container named
  `magma-debug-<fuzzer>-<target>-<program>` (or `DEBUG_CONTAINER`),
  mounts the repository at `/workspace/magma` (plus the git common dir
  for worktrees), writes connection details to `<SHARED>/debug.env`,
  and skips campaign execution and archiving.
- Intended for agent-driven inspection: the agent execs into the
  container and replays/patches the target interactively
  (`skills/magma/SKILL.md` documents the flow); stale containers are
  removed on exit.
- Upstream v1.2 has no debug-mode concept.

### 6. Captain hardening

- `tools/captain/run.sh` (+62): `IMAGE_PREFIX` image-name isolation,
  per-pair `*_build_exitcode` and campaign `*_exitcode` logging, and a
  `CAMPAIGN_TIMEOUT` wrapper around each campaign.
- `tools/captain/start.sh` (+68): preserves the real exit status of the
  campaign container (cleanup no longer masks failures with `exit 0`).
- `tools/captain/build.sh`: passes `--build-arg max_jobs` and
  `source_coverage`; honors `IMAGE_PREFIX`.
- Target `build.sh` files: `make -j${MAX_JOBS:-$(nproc)}` so
  memory-heavy fuzzers (e.g. `aflplusplus_lto_asan` ThinLTO links) can
  bound parallelism; unset keeps upstream behavior.
- `tools/captain/runonce.sh` (+55): single-input replay helper consumed
  by the MCP `magma_run_testcase` tool.
- `tools/captain/extract2.sh` (+39): testcase-analysis output consumed
  by MCP results parsing; `captainrc.fullmatrix` is a ready-made 60 s
  full-matrix config.
- `magma/run.sh` (+21): fixes seed pruning for per-program corpus dirs,
  preserves the campaign pipeline exit code (timeout-reached campaigns
  exit 0, real fuzzer failures propagate), fixes `$SHARED/log`
  permissions, and hooks in the source-coverage replay.
- `tools/captain/captainrc` (+28): documents the new variables
  (`POC_MODE`, `POC_TARGETS`, `POC_FUZZER`, `SOURCE_COVERAGE`,
  `DEBUG_MODE`, `DEBUG_CONTAINER`).

### 7. Report/benchd robustness

- `tools/benchd/exp2json.py`: pins the multiprocessing **fork** context
  (Python 3.14 switched the default start method to `forkserver`,
  which cannot spawn this script's `Pool(initializer=...)` workers;
  no-op on older Pythons such as Ubuntu 18.04's 3.6).
- `tools/report_df/main.py`: second-granular durations + `--title`.
- `CoverageData.py`: empty-coverage pages instead of `exit(1)`.
- `MatplotlibPlotter.py`: skip targets with no triggered data;
  fuzzer color cycling beyond the 10-color default prop cycle.
- `tools/report_df/requirements.txt` removed (deps moved to
  `tools/requirements.txt`).

### 8. Misc

- `pytest.ini`, `.gitignore` additions, `tools/requirements.txt`
  (+20), `mmcp/README.md`,
  `mmcp/examples/http_client.py`, fuzzer `runonce.sh` scripts,
  minor `fuzzers/{libfuzzer}/run.sh` and
  `fuzzers/honggfuzz/instrument.sh` tweaks.

### Bottom line (Part I)

HexHive `v1.2` is the untouched upstream baseline; `v1.2-next` layers
agent-facing tooling (MCP server + CLI + skills), a coverage pipeline,
PoC mode, debug mode, and campaign/report robustness fixes on top of
it, without changing what is being fuzzed (same targets, same bugs,
same toolchain era).

---

# Part II — `v1.4` vs `hexhive/v1.2`

## Relationship

| | |
|---|---|
| `hexhive/v1.2` HEAD | `75d1ae7b` (same merge base as Part I) |
| Behind HexHive | **0 commits** — strict descendant |
| Ahead of HexHive | 76 commits |
| Tree delta | 7,417 files, **+145,680 / −1,793** lines |

`v1.4` contains everything listed in Part I (the same agent tooling,
PoC mode, debug mode, coverage pipeline, Captain hardening and report
fixes — historically the same feature line, before `v1.2-next` was
split off) **plus** a full modernization of the benchmark itself.
This part only describes what `v1.4` adds **on top of Part I's
feature set**.

## 1. Ubuntu 24.04 base image

- `docker/Dockerfile`: `FROM ubuntu:24.04` (single stage), with
  build-time `USER_ID`/`GROUP_ID` handling and fuzzer `postinstall.sh`
  support. HexHive v1.2 builds on Ubuntu 18.04.

## 2. Target/fuzzer migration (2026 snapshots)

- 9 targets re-pinned to start-of-2026 snapshots, fetched via the
  release system below instead of per-target `fetch.sh`.
- Bug patches grown from **138 → 190** (`patches/bugs/`): new bugs and
  forward-ports with canaries, plus new fuzzing harnesses and a large
  PHP corpus addition.
- Deprecated target patches moved to `patches/graveyard/` (28 files).
- 3 dead fuzzers (`angora`, `symcc_afl`, `symcc_analysis`) moved to
  `fuzzers/graveyard/` → **23 active fuzzers** (HexHive: 26).

## 3. Release/version system

- `targets/*/releases` (9 files): per-target git URLs with
  `PIONEER` (pinned `STABLE_COMMIT`) and `LEGACY_YYYY` (tag) entries.
- `magma/fetch_target.sh` fetches by version; captain forwards
  `TARGET_VERSION` as a Docker build-arg (default `PIONEER`).
- `tools/releasegen/` generates the releases files (yearly anchors +
  `STABLE_COMMIT`), exposed through the MCP release API
  (`magma_generate_target_release`) — **kept** on this branch, unlike
  `v1.2-next` where the release generator was removed.

## 4. Notes vs Part I

- CLI defaults: the CLI code is identical, but the default target
  version is data-driven — targets without a `releases` file resolve to
  `FIXED` (v1.2-next: fixed `fetch.sh` sources), targets with releases
  resolve to `PIONEER` (v1.4: 2026 pinned snapshots).

## Bottom line (Part II)

`v1.4` = Part I's agent tooling **+** a modernized benchmark: 2026
target snapshots selected through a release/version system, 52 more
bug patches, Ubuntu 24.04, and a slimmed 23-fuzzer set — at the cost
of a much larger tree (corpus-heavy, +145k lines).

---

# Part III — Fuzzer versions: `v1.2-next` (Magma 2021) vs `v1.4` (Magma 2026)

Versions below were extracted from each branch's `fuzzers/*/fetch.sh`
and cross-checked against the built Docker images
(`git describe --tags` inside the container). The 26 fuzzer directories
are all accounted for: 23 fuzzer rows (variants merged into their base
row, see "Covers") plus one row for the three non-fuzzer utility
drivers (`vanilla`, `llvm_analysis`, `llvm_cov`), which track no fuzzer
version.

| Fuzzer | Covers | 2021 version | M/Y | 2026 version | M/Y |
|---|---|---|---|---|---|
| AFL | `afl`, `afl_asan`, `afl_resume` | `6103710` (2.57b-9) | 06/21 | `6103710` (2.57b-9) | 06/21 |
| AFLFast | `aflfast` | `11ec182` | 10/19 | `11ec182` | 10/19 |
| AFL++ | `aflplusplus`, `aflplusplus_lto`, `aflplusplus_lto_asan` | `458eb08` (3.13c-9) | 07/21 | `5e8278da` (4.34c-188) | 01/26 |
| Honggfuzz | `honggfuzz`, `honggfuzz_asan` | `fc6b818` (2.4-27) | 07/21 | `dfbbb38` (2.6-81) | 01/26 |
| libFuzzer | `libfuzzer` | 13.0.0 (`29cc50e1`) | 07/21 | 22.0.0 (`c2c787c1`) | 01/26 |
| Entropic | `entropic` | 13.0.0 (`29cc50e1`) | 07/21 | 22.0.0 (`c2c787c1`) | 01/26 |
| Angora † | `angora` | `3cedcac` | 10/20 | `3cedcac` (graveyard) | 10/20 |
| Eclipser | `eclipser` | unpinned (`ba1d7a5`) | 06/21 | unpinned (`ba1d7a5`) | 06/21 |
| FairFuzz | `fairfuzz` | `e529c1f` | 01/19 | `e529c1f` | 01/19 |
| InsTrim | `instrim` | `82b5635` | 06/20 | `82b5635` | 06/20 |
| K-Scheduler | `k_scheduler` | `36bc5aa` | 09/22 | `6e78fbe` | 04/23 |
| KLEE | `klee` | `df04aea` (+uclibc `9351bdc`) | 06/21 | `df04aea` (+uclibc `9351bdc`) | 06/21 |
| MOpt-AFL | `moptafl`, `moptafl_asan` | `a9a5dc5` | 01/21 | `a9a5dc5` | 01/21 |
| ParmeSan | `parmesan` | `fac5801` | 10/20 | `fac5801` | 10/20 |
| DDFuzz | `ddfuzz` | `319f702` | 02/22 | `319f702` | 02/22 |
| SymCC † | `symcc_afl`, `symcc_analysis` | `82151a6` (+AFL `6103710`) | 06/21 | `82151a6` (+AFL `6103710`, graveyard) | 06/21 |
| Utilities | `vanilla`, `llvm_analysis`, `llvm_cov` | — | — | — | — |

† Three fuzzers — Angora, `symcc_afl`, and `symcc_analysis` — ship
unchanged but were moved to `fuzzers/graveyard/` in Magma 2026 and are no
longer part of the active benchmark. The SymCC row covers both SymCC
variants (they share the pin and its AFL base).

Note on pins that fall between upstream releases: AFL++ is pinned
**between** releases on both sides — `3.13c-9-g458eb081` in Magma 2021
and `v4.34c-188-g5e8278da` (2026-01-05) in Magma 2026; Honggfuzz 2026 is
`2.6-81-gdfbbb38d` (2026-01-01), 81 commits past the 2.6 tag; libFuzzer
and Entropic 2026 pin LLVM `c2c787c1` (2026-01-01) on the 22.0.0 line.

---

# Part IV — Target versions: `v1.2-next` (Magma 2021) vs `v1.4` (Magma 2026)

Magma 2021 pins come from each target's `fetch.sh` (a git commit, or a
fossil tarball for sqlite3); Magma 2026 pins every target to its **first
commit of 2026** through the release system (`targets/*/releases`,
`PIONEER_STABLE_COMMIT`). Versions below were verified by cloning each
upstream repository and running `git describe --tags` on both pins
(sqlite3 2021 taken from the pinned tarball's `VERSION` file). php and
poppler additionally pin oniguruma (`227ec0bd` in 2021) and freetype
(`50d0033f` in 2021).

| Target | 2021 version | M/Y | 2026 version | M/Y |
|---|---|---|---|---|
| libpng | 1.6.37-36 (`a37d4836`) | 03/21 | 1.6.53-4 (`9e4e247a`) | 01/26 |
| libsndfile | 1.1.0beta1-8 (`86c9f9eb`) | 07/21 | 1.2.2-53 (`68f6c16f`) | 12/25 |
| libtiff | 4.3.0-35 (`c145a6c1`) | 06/21 | 4.7.1-92 (`65a694aa`) | 01/26 |
| libxml2 | 2.9.12-13 (`ec6e3efb`) | 07/21 | 2.15.0-36 (`eae9291a`) | 01/26 |
| lua | 5.4.3-16 (`dbdc74dc`) | 06/21 | 5.5.0-4 (`962f444a`) | 01/26 |
| openssl | 3.0.0-beta1-193 (`3bd5319b`) | 07/21 | 4.0-dev-130 (`61c87619`) | 01/26 |
| php | master/8.1-dev (`bc39abe8`) | 07/21 | master (`e49be5f8`) | 01/26 |
| poppler | 21.07.0-6 (`1d23101c`) | 06/21 | 25.12.0-78 (`47d94f39`) | 01/26 |
| sqlite3 | 3.37.0 (`8c432642`, fossil) | 07/21 | 3.51.0-485 (`6e8afa79`) | 01/26 |

Notes: every Magma 2026 pin sits on the first-commit-of-2026 snapshot
(2025-12-16 .. 2026-01-08), so most are a few commits **past** the
respective last release (e.g. libpng 4 commits after 1.6.53, libtiff 92
after 4.7.1). openssl and php track the 4.0 / 8.x development lines,
which had no tagged release at pin time, so no release version can be
attributed. Through the release system, historical anchors
(`LEGACY_YYYY`) are generatable for any year — libpng already carries
2021-2026 anchors.

---

# Part V — Bug-patch status: `v1.2-next` (Magma 2021) → `v1.4` (Magma 2026)

Patch status was derived by comparing every bug patch between the two
branches: identical file content = applied cleanly; changed content =
re-ported (hunk realignment); moved to `patches/graveyard/` =
graveyarded; present only in `v1.4` = newly introduced with the 2026
update.

**Totals: 138 patches in 2021 → 62 applied unchanged, 63 re-ported,
13 graveyarded; 65 added in 2026 → 190 active in 2026.**

Markers: `*` = re-ported, `†` = graveyarded, `‡` = new in 2026;
plain = applied without modification.

| Target | Bug patch names |
|---|---|
| libpng | †PNG001, \*PNG002, \*PNG003, PNG004, PNG005, \*PNG006, PNG007, ‡PNG008, ‡PNG009, ‡PNG010, ‡PNG011 |
| libsndfile | SND001, SND002, SND004, SND005, SND006, SND007, SND010, SND012, SND013, SND014, SND015, SND016, SND017, SND020, SND022, SND023, SND024, SND025, ‡SND026-036 |
| libtiff | \*TIF001-014, ‡TIF015-027 |
| libxml2 | XML001, XML006, XML016, \*XML011, \*XML012, \*XML015, \*XML017, †XML002-005, †XML007-010, †XML013, †XML014, ‡XML018-022 |
| lua | \*LUA001, LUA002, \*LUA003, \*LUA004, ‡LUA005-009 |
| openssl | \*SSL001, SSL002, \*SSL003, \*SSL004, SSL005, SSL006, SSL007, \*SSL008, \*SSL009, \*SSL010, SSL011, SSL012, SSL013, SSL014, \*SSL015, SSL016, SSL017, \*SSL018, \*SSL019, \*SSL020, ‡SSL021-026 |
| php | \*PHP001, PHP002, PHP003, PHP004, PHP005, PHP006, PHP007, PHP008, PHP009, \*PHP010, PHP011, \*PHP012, \*PHP013, \*PHP014, \*PHP015, \*PHP016, ‡PHP017-023 |
| poppler | PDF001, \*PDF002, \*PDF003, \*PDF004, PDF005, \*PDF006, \*PDF007, PDF008, \*PDF009, PDF010, PDF011, PDF012, \*PDF013, PDF014, \*PDF015, PDF016, \*PDF017, \*PDF018, \*PDF019, \*PDF020, PDF021, \*PDF022, ‡PDF023-031 |
| sqlite3 | \*SQL001, \*SQL002, \*SQL003, SQL004, SQL005, \*SQL006, \*SQL007, SQL008, SQL009, SQL010, SQL011, †SQL012, \*SQL013, \*SQL014, \*SQL015, SQL016, \*SQL017, SQL018, SQL020, †SQL019, ‡SQL021-025 |

The graveyard also contains pre-2021 legacy entries that predate this
update and are not listed as transitions above: HexHive-era bug IDs
(`AAH*`, `MAE*`, `JCH*`), `SND003`, `SND021`, and old setup patches.
