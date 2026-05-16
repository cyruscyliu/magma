# Graveyard — angora

**Graveyarded:** 2026-05-16  
**Snapshot year attempted:** 2026

## Reason

Angora requires LLVM 7 (and optionally LLVM 11) as a prebuilt binary,
neither of which is packaged for Ubuntu 24.04 (Noble). Additionally,
its build scripts download an `x86_64` prebuilt LLVM binary and a
Rust toolchain installer (`rustup-init`) that cannot execute on the
arm64 build-check host (`Exec format error`).

No fix is possible without either:
- a major upstream port of Angora's LLVM pass to LLVM 14+, or
- an x86_64 build environment.

## Failed attempts summary

| Attempt | Failure |
|---------|---------|
| 1 | `python-pip` not available on Noble |
| 2 | Non-idempotent fetch (repo already exists) |
| 3 | `rustup-init: cannot execute binary file: Exec format error` (x86_64 binary on arm64) |
| 4–5 | Downloads `clang+llvm-7.0.1-x86_64-*` prebuilt — incompatible with arm64 host |
| 6–9 | LLVM pass incompatible with LLVM 14/18 APIs |
| 10–12 | LLVM 11 not packaged for Noble (`llvm-toolchain-noble-11` has no Release file) |
