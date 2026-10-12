# libpng graveyard patches

`PNG001` was retired for libpng `PIONEER` 2026.

Reason: the upstream function targeted by the patch, `png_check_chunk_length`, no longer exists at commit `9e4e247`.
Per Magma policy, we do not semantically rebase/backport deprecated-path bug patches; the patch is archived here instead.
