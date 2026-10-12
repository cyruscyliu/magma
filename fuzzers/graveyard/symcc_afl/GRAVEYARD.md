# Graveyard — symcc_afl

**Graveyarded:** 2026-06-01  
**Snapshot year attempted:** 2026

## Reason

SymCC requires LLVM 9 (clang-9) as its compiler backend, which is no longer packaged
for Ubuntu 24.04 (Noble). This is a hard architectural dependency — SymCC's LLVM pass
is tightly coupled to the LLVM 9 API and cannot be compiled against LLVM 14+
without a major upstream port of SymCC itself.

Additionally, `symcc_afl` depends on the AFL++ `llvm_mode/` subdirectory, which was
removed in AFL++ 4.x and replaced by a different instrumentation architecture.

No fix is possible within `fuzzers/symcc_afl/` alone without:
- Porting SymCC's LLVM pass to LLVM 14+, or
- Porting the qsym backend CMake build to a modern LLVM, or
- An Ubuntu LTS that still packages `clang-9`.

## Failed attempts summary

| Attempt | Failure |
|---------|---------|
| 1 | `E: Package 'clang-9' has no installation candidate` |
| 2 | `error: externally-managed-environment` (pip install outside venv) |
| 3 | `fatal: destination path 'repo' already exists` (non-idempotent fetch) |
| 4 | `make: *** llvm_mode: No such file or directory` (AFL++ 4.x removed llvm_mode) |
| 5 | `CMake Error … Cannot find source file: qsym/qsym/pintool/expr.cpp` |
| 6 | `LLVMSupport` link failure: `zstd::libzstd_shared` target not found |
| 7 | `lock file version 4 requires -Znext-lockfile-bump` (Cargo/Rust toolchain mismatch) |
| 8–9 | No default rustup toolchain; `build.sh` lacks persistent toolchain env |
| 10 | `libcxx isn't a known project` (renamed to LLVM runtimes in LLVM 14+) |
