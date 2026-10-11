from mmcp.core import paths


def test_list_target_names_requires_configrc(magma_root):
    (magma_root / "targets" / "notarget").mkdir()
    assert paths.list_target_names() == ["libpng", "libtiff"]


def test_list_fuzzer_names_requires_run_sh(magma_root):
    (magma_root / "fuzzers" / "nofuzz").mkdir()
    assert paths.list_fuzzer_names() == ["aflplusplus"]


def test_list_bug_ids(magma_root):
    assert paths.list_bug_ids("libpng") == ["PNG001", "PNG002"]
    assert paths.list_bug_ids("missing") == []


def test_list_poc_files(magma_root):
    pocs = magma_root / "targets" / "libpng" / "pocs"
    pocs.mkdir()
    (pocs / "PNG001.crash").write_text("x")
    assert paths.list_poc_files("libpng") == ["PNG001.crash"]
    assert paths.list_poc_files("libtiff") == []


def test_list_corpus_files(magma_root):
    corpus = magma_root / "targets" / "libpng" / "corpus" / "libpng_read_fuzzer"
    corpus.mkdir(parents=True)
    (corpus / "seed_1.png").write_text("x")
    assert paths.list_corpus_files("libpng", "libpng_read_fuzzer") == ["seed_1.png"]


def test_magma_env_override(magma_root, monkeypatch):
    monkeypatch.setenv("MAGMA", str(magma_root))
    assert paths._find_magma_root() == magma_root.resolve()


def test_helper_paths(magma_root):
    assert paths.target_configrc("libpng") == (
        magma_root / "targets" / "libpng" / "configrc"
    )
    assert paths.target_releases("libpng") == (
        magma_root / "targets" / "libpng" / "releases"
    )
    assert paths.bug_patch_path("libpng", "PNG001") == (
        magma_root / "targets" / "libpng" / "patches" / "bugs" / "PNG001.patch"
    )
    assert paths.fuzzer_script("aflplusplus", "runonce.sh") == (
        magma_root / "fuzzers" / "aflplusplus" / "runonce.sh"
    )


def test_list_dirs_missing_root(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "TARGETS_DIR", tmp_path / "nope")
    monkeypatch.setattr(paths, "FUZZERS_DIR", tmp_path / "nope")
    assert paths.list_target_names() == []
    assert paths.list_fuzzer_names() == []
