"""Exercise the public CLI in subprocesses; Docker is replaced at the boundary."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "magma-cli"


@pytest.fixture
def docker(tmp_path):
    binary = tmp_path / "bin" / "docker"
    binary.parent.mkdir()
    binary.write_text("""#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
args = sys.argv[1:]
with open(os.environ["DOCKER_CALLS"], "a") as log:
    log.write(json.dumps(args) + "\\n")
if args[:2] == ["image", "inspect"]:
    if os.environ.get("NO_IMAGE"):
        print("image missing", file=sys.stderr)
        sys.exit(1)
    labels = {"org.magma.cli.release": "wrong"} if os.environ.get("WRONG_RELEASE") else {}
    if os.environ.get("PLAIN_IMAGE"):
        labels["org.magma.cli.canary-mode"] = "plain"
    print(json.dumps([{"Config": {"Env": ["FUZZER=/magma/fuzzers/aflplusplus", "TARGET=/magma/targets/libpng"], "Labels": labels}}]))
elif args[0] == "build":
    print("build progress on stdout")
    print("build progress on stderr", file=sys.stderr)
    sys.exit(int(os.environ.get("BUILD_EXIT", "0")))
elif args[0] == "run":
    mounts = [args[i + 1] for i, arg in enumerate(args[:-1]) if arg == "--volume"]
    testcase = next((m for m in mounts if m.endswith(":/magma_input/testcase:ro")), None)
    if testcase:
        content = Path(testcase.removesuffix(":/magma_input/testcase:ro")).read_text()
        print("target diagnostics", file=sys.stderr)
        if content == "slow":
            time.sleep(30)
        if content in ("trigger", "crash"):
            print("PNG002 reached 7 triggered 2")
            print("PNG003 reached 2 triggered 1")
        else:
            print("PNG002 reached 1 triggered 0")
        sys.exit(1 if content == "crash" else 125 if content == "error" else 0)
    print("campaign logs")
    sys.exit(int(os.environ.get("RUN_EXIT", "0")))
""")
    binary.chmod(0o755)
    env = {
        **os.environ,
        "PATH": str(binary.parent) + os.pathsep + os.environ["PATH"],
        "DOCKER_CALLS": str(tmp_path / "docker-calls.jsonl"),
        "MAGMA": "/not/this/repository",
    }
    return env


def invoke(*args, env=None, cwd=None):
    result = subprocess.run(
        [sys.executable, str(CLI), *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        timeout=20,
    )
    data = json.loads(result.stdout)
    assert result.returncode == data["exit_code"]
    assert data["schema_version"] == 1
    return result, data


def calls(env):
    path = Path(env["DOCKER_CALLS"])
    return (
        [json.loads(line) for line in path.read_text().splitlines()]
        if path.exists()
        else []
    )


COMMON = ["--fuzzer", "aflplusplus", "--target", "libpng"]
PROGRAM = [*COMMON, "--program", "libpng_read_fuzzer"]


def test_discovery_works_outside_repo_without_mcp(docker, tmp_path):
    _, data = invoke("list", "targets", env=docker, cwd=tmp_path)
    png = next(t for t in data["items"] if t["name"] == "libpng")
    assert "libpng_read_fuzzer" in png["programs"]
    assert calls(docker) == []
    _, fuzzers = invoke("list", "fuzzers", env=docker)
    assert all(f["name"] != "graveyard" for f in fuzzers["items"])


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["unknown"],
        ["list", "programs"],
        ["build", "--fuzzer", "../escape", "--target", "libpng"],
        ["build", *COMMON, "--target-version", "NOT_REAL"],
        ["run", *PROGRAM, "--workdir", "unused", "--timeout", "0"],
        ["run", *PROGRAM, "--workdir", "unused", "--poll", "0"],
        ["run", *COMMON, "--program", "missing", "--workdir", "unused"],
    ],
)
def test_invalid_arguments_are_json_without_docker(arguments, docker):
    result, data = invoke(*arguments, env=docker)
    assert result.returncode == 2
    assert data["error"]
    assert calls(docker) == []


def test_build_version_adapter_and_dry_run(docker, tmp_path):
    log = tmp_path / "new-dir" / "build.log"
    _, data = invoke(
        "build",
        *COMMON,
        "--source-coverage",
        "--canary-mode",
        "fixes",
        "--harden",
        "--no-cache",
        "--dry-run",
        "--log-file",
        log,
        env=docker,
    )
    command = data["commands"][0]
    assert (
        "fixes=1" in command
        and "source_coverage=1" in command
        and "harden=1" in command
    )
    assert "--no-cache" in command
    assert data["release"] in data["image"]
    assert data["target_version"] == "PIONEER"
    assert "target_version=PIONEER" in command
    assert not log.parent.exists()
    assert calls(docker) == []


def test_build_streams_logs_and_propagates_failure(docker, tmp_path):
    docker["BUILD_EXIT"] = "17"
    log = tmp_path / "build.log"
    result, data = invoke("build", *COMMON, "--log-file", log, env=docker)
    assert result.returncode == 1 and data["process_exit_code"] == 17
    assert "build progress on stdout" in result.stderr
    assert "build progress on stderr" in log.read_text()
    assert "commands" not in data


def test_run_quotes_paths_uses_config_args_and_creates_output(docker, tmp_path):
    workdir = tmp_path / "run with spaces"
    result, data = invoke(
        "run",
        *PROGRAM,
        "--workdir",
        workdir,
        "--args=-M @@ output",
        "--fuzz-args=-m none",
        "--affinity",
        "0,2-3",
        env=docker,
    )
    assert result.returncode == 0
    command = next(c for c in calls(docker) if c[0] == "run")
    assert str(workdir) + ":/magma_shared" in command
    assert "ARGS=-M @@ output" in command
    assert "FUZZARGS=-m none" in command
    assert "--network=none" in command and "--rm" in command
    assert "campaign logs" in Path(data["log_file"]).read_text()


def test_default_program_arguments_from_config(docker, tmp_path):
    _, config = invoke("list", "programs", "--target", "libtiff", env=docker)
    expected = next(p["args"] for p in config["items"] if p["name"] == "tiffcp")
    _, data = invoke(
        "run",
        "--fuzzer",
        "aflplusplus",
        "--target",
        "libtiff",
        "--program",
        "tiffcp",
        "--workdir",
        tmp_path / "output",
        "--dry-run",
        env=docker,
    )
    assert f"ARGS={expected}" in data["commands"][0]
    assert expected


def test_dry_run_does_not_create_workdir(docker, tmp_path):
    workdir = tmp_path / "output"
    _, data = invoke("run", *PROGRAM, "--workdir", workdir, "--dry-run", env=docker)
    assert data["status"] == "planned"
    assert not workdir.exists() and calls(docker) == []


def test_existing_workdir_is_preserved(docker, tmp_path):
    (tmp_path / "finding").write_text("keep")
    result, _ = invoke("run", *PROGRAM, "--workdir", tmp_path, env=docker)
    assert result.returncode == 2
    assert (tmp_path / "finding").read_text() == "keep"
    assert calls(docker) == []


@pytest.mark.parametrize("key", ["NO_IMAGE", "WRONG_RELEASE"])
def test_image_preflight_leaves_no_output(key, docker, tmp_path):
    docker[key] = "1"
    workdir = tmp_path / "output"
    result, data = invoke("run", *PROGRAM, "--workdir", workdir, env=docker)
    assert result.returncode == 1 and data["status"] == "error"
    assert not workdir.exists()
    assert not any(c[0] == "run" for c in calls(docker))


def test_run_failure_is_not_success(docker, tmp_path):
    docker["RUN_EXIT"] = "23"
    result, data = invoke("run", *PROGRAM, "--workdir", tmp_path / "output", env=docker)
    assert result.returncode == 1 and data["process_exit_code"] == 23


@pytest.mark.parametrize(
    "content,expected,status",
    [
        ("clean", 0, "clean"),
        ("trigger", 0, "triggered"),
        ("crash", 0, "triggered"),
        ("error", 1, "failed"),
    ],
)
def test_replay_classifies_oracle_and_exit_codes(
    content, expected, status, docker, tmp_path
):
    path = tmp_path / "input ' with spaces $(ignored)"
    path.write_text(content)
    log = tmp_path / "replay.log"
    result, data = invoke(
        "replay", *PROGRAM, "--input", path, "--log-file", log, env=docker
    )
    assert result.returncode == expected
    replay = data["results"][0]
    assert replay["status"] == status
    assert replay["triggered_bugs"] == (
        ["PNG002", "PNG003"] if status == "triggered" else []
    )
    assert "target diagnostics" in log.read_text()
    command = next(c for c in calls(docker) if c[0] == "run")
    assert str(path) + ":/magma_input/testcase:ro" in command
    assert str(path) not in command[-1]


def test_replay_directory_and_expectation(docker, tmp_path):
    directory = tmp_path / "inputs"
    directory.mkdir()
    (directory / "a").write_text("trigger")
    (directory / "b").write_text("clean")
    result, data = invoke(
        "replay",
        *PROGRAM,
        "--input",
        directory,
        "--input",
        directory / "a",
        "--expect-bug",
        "PNG002",
        env=docker,
    )
    assert result.returncode == 3
    assert len(data["results"]) == 2
    assert data["results"][1]["status"] == "expectation_failed"


def test_replay_timeout_removes_container(docker, tmp_path):
    path = tmp_path / "input"
    path.write_text("slow")
    result, data = invoke(
        "replay", *PROGRAM, "--input", path, "--timeout", "0.2s", env=docker
    )
    assert result.returncode == 1
    assert data["results"][0]["status"] == "timeout"
    assert any(c[:2] == ["rm", "--force"] for c in calls(docker))


def test_refuses_to_overwrite_log(docker, tmp_path):
    log = tmp_path / "existing.log"
    log.write_text("keep")
    result, _ = invoke("build", *COMMON, "--log-file", log, env=docker)
    assert result.returncode == 1 and log.read_text() == "keep"
    assert calls(docker) == []


@pytest.mark.parametrize("fuzzer_exit,expected", [(0, 0), (124, 0), (23, 23)])
def test_campaign_script_preserves_fuzzer_failures(fuzzer_exit, expected, tmp_path):
    shared, target, fuzzer, magma, out, binaries = [
        tmp_path / name
        for name in ("shared", "target", "fuzzer", "magma", "out", "bin")
    ]
    for path in (shared, fuzzer, magma, out, binaries, target / "corpus" / "driver"):
        path.mkdir(parents=True)
    (target / "corpus" / "driver" / "seed").write_text("seed")
    scripts = {
        magma / "runonce.sh": "exit 0",
        fuzzer / "run.sh": f"exit {fuzzer_exit}",
        out / "monitor": "exit 0",
        binaries / "multilog": 'mkdir -p "${@: -1}"; cat >/dev/null',
    }
    for path, body in scripts.items():
        path.write_text("#!/bin/bash\n" + body + "\n")
        path.chmod(0o755)
    env = {
        **os.environ,
        "SHARED": str(shared),
        "TARGET": str(target),
        "FUZZER": str(fuzzer),
        "MAGMA": str(magma),
        "OUT": str(out),
        "PROGRAM": "driver",
        "POLL": "1",
        "TIMEOUT": "1s",
        "SOURCE_COVERAGE": "",
        "PATH": str(binaries) + os.pathsep + os.environ["PATH"],
    }
    result = subprocess.run(
        ["bash", str(ROOT / "magma" / "run.sh")],
        env=env,
        check=False,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == expected, result.stderr


def test_missing_and_empty_replay_inputs(docker, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    for path in (tmp_path / "missing", empty):
        result, data = invoke("replay", *PROGRAM, "--input", path, env=docker)
        assert result.returncode == 2 and data["status"] == "error"
    assert calls(docker) == []


def test_sigterm_cleans_up_replay_container(docker, tmp_path):
    import time

    path = tmp_path / "input"
    path.write_text("slow")
    process = subprocess.Popen(
        [sys.executable, str(CLI), "replay", *PROGRAM, "--input", str(path)],
        env=docker,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.monotonic() + 5
        while not any(c[0] == "run" for c in calls(docker)):
            assert time.monotonic() < deadline
            time.sleep(0.01)
        process.terminate()
        stdout, stderr = process.communicate(timeout=8)
        assert process.returncode == 130, stderr
        assert json.loads(stdout)["status"] == "cancelled"
        assert any(c[:2] == ["rm", "--force"] for c in calls(docker))
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()


def test_expected_bug_requires_canaries(docker, tmp_path):
    docker["PLAIN_IMAGE"] = "1"
    path = tmp_path / "input"
    path.write_text("clean")
    result, data = invoke(
        "replay", *PROGRAM, "--input", path, "--expect-bug", "PNG002", env=docker
    )
    assert result.returncode == 1
    assert "canaries" in data["error"]
    assert not any(c[0] == "run" for c in calls(docker))


@pytest.fixture
def captain_workdir(tmp_path):
    """A minimal Captain workdir: one campaign tarball with monitor samples."""
    workdir = tmp_path / "workdir"
    campaign = workdir / "ar" / "aflplusplus" / "libpng" / "libpng_read_fuzzer" / "0"
    campaign.mkdir(parents=True)
    monitor = tmp_path / "monitor"
    monitor.mkdir()
    (monitor / "0").write_text("PNG001_R,PNG001_T\n0,0\n")
    (monitor / "5").write_text("PNG001_R,PNG001_T\n3,1\n")
    subprocess.run(
        ["tar", "-cf", str(campaign / "ball.tar"), "-C", str(tmp_path), "monitor"],
        check=True,
    )
    return workdir


def run_cli(argv, **kwargs):
    return subprocess.run(
        [sys.executable, str(CLI), *argv],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
        **kwargs,
    )


def test_report_requires_captain_workdir(tmp_path):
    empty = tmp_path / "not-a-workdir"
    empty.mkdir()
    result = run_cli(["report", "--workdir", str(empty)], timeout=60)
    data = json.loads(result.stdout)
    assert result.returncode == 2
    assert data["status"] == "error" and "ar/" in data["error"]


def test_report_refuses_existing_output(captain_workdir, tmp_path):
    output = tmp_path / "report"
    output.mkdir()
    (output / "occupied").write_text("x")
    result = run_cli(
        ["report", "--workdir", str(captain_workdir), "--output", str(output)],
        timeout=60,
    )
    data = json.loads(result.stdout)
    assert result.returncode == 2
    assert data["status"] == "error" and "new or empty" in data["error"]


def test_report_generates_pages_and_html(captain_workdir, tmp_path):
    output = tmp_path / "report"
    result = run_cli(
        [
            "report",
            "--workdir",
            str(captain_workdir),
            "--output",
            str(output),
            "--trials",
            "1",
            "--duration",
            "5s",
        ],
        timeout=600,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["status"] == "completed" and data["trials"] == 1
    pages = {Path(page).name for page in data["pages"]}
    assert {"index.html", "aflplusplus.html", "libpng.html", "coverage.html"} <= pages
    index = (output / "index.html").read_text()
    assert "{% raw %}" not in index
    assert "css/report.css" in index and "<!DOCTYPE html>" in index
    assert (output / "css" / "report.css").is_file()
    summary = json.loads((output / "bench.json").read_text())
    assert summary["results"]["aflplusplus"]["libpng"]["libpng_read_fuzzer"]["0"][
        "triggered"
    ] == {"PNG001": 5}
