# Graveyard — symcc_analysis

**Graveyarded:** 2026-06-01  
**Snapshot year attempted:** 2026

## Reason

SymCC requires LLVM 9 (clang-9) as its compiler backend, which is no longer packaged
for Ubuntu 24.04 (Noble). `symcc_analysis` builds SymCC's analysis mode (concolic
execution without AFL), which shares the same hard LLVM 9 dependency.

The `sym++` compiler wrapper crashes (SIGSEGV, exit 139) when built against LLVM 14+
because SymCC's LLVM pass uses internal APIs removed in LLVM 12. The `libc++`
subproject was also renamed to an LLVM runtime in LLVM 14+, breaking the CMake
configuration entirely.

No fix is possible within `fuzzers/symcc_analysis/` alone without:
- Porting SymCC's LLVM pass to LLVM 14+, or
- An Ubuntu LTS that still packages `clang-9`.

## Failed attempts summary

| Attempt | Failure |
|---------|---------|
| 1–2 | `E: Package 'clang-9' has no installation candidate` |
| 3 | `fetch.sh must be executed first` (build ordering issue in fix attempt) |
| 4–5 | `LLVMSupport` link failure: `zstd::libzstd_shared` target not found |
| 6 | `error: failed to parse lock file` (Cargo.lock version incompatible with installed Rust) |
| 7 | `libcxx isn't a known project` (renamed to LLVM runtimes in LLVM 14+) |
| 8 | `Configuring incomplete, errors occurred during libc++ configuration` |
| 9 | `clang frontend command failed with exit code 139` compiling RustDemangle.cpp via sym++ |
