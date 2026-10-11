import pytest

from mmcp.core import config_parser


def test_parse_configrc(magma_root):
    cfg = config_parser.parse_configrc("libpng")
    assert cfg["programs"] == ["libpng_read_fuzzer"]
    assert cfg["program_args"] == {"libpng_read_fuzzer": "@@"}


def test_parse_configrc_multi_program(magma_root):
    cfg = config_parser.parse_configrc("libtiff")
    assert cfg["programs"] == ["tiff_read_rgba_fuzzer", "tiffcp"]
    assert cfg["program_args"]["tiffcp"] == "-M @@ tmp.out"
    assert cfg["program_args"]["tiff_read_rgba_fuzzer"] == ""


def test_parse_configrc_missing_target(magma_root):
    with pytest.raises(FileNotFoundError):
        config_parser.parse_configrc("nosuch")


def test_parse_releases(magma_root):
    f = magma_root / "targets" / "libpng" / "releases"
    f.write_text(
        'libpng_PIONEER="https://example.com/libpng.git"\n'
        'libpng_PIONEER_STABLE_COMMIT="abc123"\n'
        'libpng_LEGACY_2024="https://example.com/libpng.git"\n'
        'libpng_LEGACY_2024_TAG="v1.6.37"\n'
    )
    rels = config_parser.parse_releases("libpng")
    assert rels[0]["name"] == "PIONEER"
    assert rels[0]["url"] == "https://example.com/libpng.git"
    assert rels[0]["ref_type"] == "commit"
    assert rels[0]["ref"] == "abc123"
    assert rels[1]["name"] == "LEGACY_2024"
    assert rels[1]["ref_type"] == "tag"
    assert rels[1]["ref"] == "v1.6.37"


def test_parse_releases_missing_file(magma_root):
    assert config_parser.parse_releases("libpng") == []


def test_parse_captainrc(magma_root):
    rc = magma_root / "tools" / "captain" / "captainrc"
    rc.write_text(
        "WORKDIR=./workdir\n"
        "REPEAT=3\n"
        "TIMEOUT=24h\n"
        "POLL=5\n"
        "FUZZERS=(aflplusplus honggfuzz)\n"
        "CANARY_MODE=1\n"
    )
    cfg = config_parser.parse_captainrc(rc)
    assert cfg["workdir"] == "./workdir"
    assert cfg["repeat"] == 3
    assert cfg["timeout"] == "24h"
    assert cfg["poll"] == 5
    assert cfg["fuzzers"] == ["aflplusplus", "honggfuzz"]
    assert cfg["canary_mode"] == 1
    assert cfg["target_version"] == "PIONEER"
    assert cfg["tmpfs_size"] == "50g"
    assert cfg["poc_mode"] == 0
    assert cfg["isan"] is False


def test_parse_captainrc_missing(magma_root):
    with pytest.raises(FileNotFoundError):
        config_parser.parse_captainrc(magma_root / "nope")


def test_get_all_targets_config(magma_root):
    cfg = config_parser.get_all_targets_config()
    assert set(cfg) == {"libpng", "libtiff"}
    assert cfg["libpng"]["programs"] == ["libpng_read_fuzzer"]
