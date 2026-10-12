"""Agent-facing build, campaign and replay commands using only the stdlib."""

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RELEASE = "v1.4"
SCHEMA_VERSION = 1


class CLIError(Exception):
    def __init__(self, message, code=2):
        super().__init__(message)
        self.code = code


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CLIError(message)


def duration(value):
    if not re.fullmatch(r"\d+(?:\.\d+)?[smhd]?", value):
        raise argparse.ArgumentTypeError(
            "use a positive duration such as 30s, 10m or 1h"
        )
    number = float(value[:-1] if value[-1].isalpha() else value)
    if number <= 0:
        raise argparse.ArgumentTypeError("duration must be positive")
    return value


def seconds(value):
    return float(value[:-1] if value[-1].isalpha() else value) * {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
    }.get(value[-1], 1)


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def parser():
    p = Parser(
        prog="magma-cli",
        description="Build, run and replay Magma. Results: JSON on stdout; logs: stderr.",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"magma-cli schema={SCHEMA_VERSION} release={RELEASE}",
    )
    commands = p.add_subparsers(dest="command", required=True)
    listing = commands.add_parser(
        "list",
        help="Discover branch-local fuzzers, targets, programs, bugs and versions",
    )
    listing.add_argument(
        "entity", choices=("fuzzers", "targets", "programs", "bugs", "versions")
    )
    listing.add_argument("--target")
    for name in ("build", "run", "replay"):
        c = commands.add_parser(
            name,
            help={
                "build": "Build a fuzzer/target Docker image",
                "run": "Run one foreground fuzzing campaign",
                "replay": "Replay files through the Magma bug oracle",
            }[name],
        )
        c.add_argument("--fuzzer", required=True)
        c.add_argument("--target", required=True)
        c.add_argument(
            "--target-version",
            default="default",
            help="default selects this branch's snapshot; see list versions",
        )
        c.add_argument(
            "--image",
            help="Override the version-specific image name (also accepts existing Captain images)",
        )
        c.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the plan without Docker calls or filesystem changes",
        )
        c.add_argument("--log-file", type=Path, help="Also save subprocess logs here")
        if name == "build":
            c.add_argument(
                "--canary-mode",
                choices=("canaries", "plain", "fixes"),
                default="canaries",
            )
            c.add_argument("--isan", action="store_true")
            c.add_argument("--harden", action="store_true")
            c.add_argument("--source-coverage", action="store_true")
            c.add_argument("--no-cache", action="store_true")
        else:
            c.add_argument("--program", required=True)
            c.add_argument(
                "--args",
                help="Program arguments; defaults to target configrc. Use --args='-x @@' for flags",
            )
            if name == "run":
                c.add_argument(
                    "--workdir",
                    type=Path,
                    required=True,
                    help="New or empty directory for findings, monitor samples and logs",
                )
                c.add_argument("--timeout", type=duration, default="1m")
                c.add_argument("--poll", type=positive_int, default=5)
                c.add_argument(
                    "--fuzz-args",
                    default="",
                    help="Fuzzer arguments; use --fuzz-args='-x /path' for flags",
                )
                c.add_argument("--affinity", help="CPU list, e.g. 0,2-3")
            else:
                c.add_argument(
                    "--input",
                    type=Path,
                    action="append",
                    required=True,
                    help="File or directory (recursive); may be repeated",
                )
                c.add_argument(
                    "--expect-bug", help="Require this bug to trigger for every input"
                )
                c.add_argument(
                    "--timeout",
                    type=duration,
                    default="10s",
                    help="Wall-clock limit per replay, including container startup",
                )
    return p


def names(kind, marker):
    return sorted(
        d.name for d in (ROOT / kind).iterdir() if d.is_dir() and (d / marker).is_file()
    )


def target_dir(target):
    if target not in names("targets", "configrc"):
        raise CLIError(f"Unknown target: {target}; use list targets")
    return ROOT / "targets" / target


def bash_values(script, path):
    result = subprocess.run(
        ["bash", "-c", script, "magma-cli", str(path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=ROOT,
    )
    if result.returncode:
        raise CLIError(f"Cannot read {path}: {result.stderr.strip()}")
    return result.stdout.split("\0")[:-1]


def programs(target):
    values = bash_values(
        'source "$1"; for p in "${PROGRAMS[@]}"; do v="${p}_ARGS"; printf "%s\\0%s\\0" "$p" "${!v}"; done',
        target_dir(target) / "configrc",
    )
    return dict(zip(values[::2], values[1::2]))


def versions(target):
    directory = target_dir(target)
    if not (directory / "releases").is_file():
        return [{"name": "FIXED", "backend": "fetch.sh", "default": True}]
    values = {}
    for line in (directory / "releases").read_text().splitlines():
        match = re.fullmatch(r'([A-Za-z0-9_]+)="([^"]*)"', line.strip())
        if match:
            values[match[1]] = match[2]
    prefix = target.replace("-", "_") + "_"
    items = []
    for key, url in values.items():
        if key.startswith(prefix) and not key.endswith(("_STABLE_COMMIT", "_TAG")):
            version = key[len(prefix) :]
            items.append(
                {
                    "name": version,
                    "url": url,
                    "ref": values.get(key + "_STABLE_COMMIT", ""),
                    "backend": "releases",
                    "default": version == "PIONEER",
                }
            )
    return sorted(items, key=lambda v: (not v["default"], v["name"]))


def selected_version(args):
    available = versions(args.target)
    name = args.target_version
    if name == "default":
        name = next((v["name"] for v in available if v["default"]), "")
    selected = next((v for v in available if v["name"] == name), None)
    if selected is None:
        raise CLIError(
            f"Unsupported target version {args.target_version!r}; available: {', '.join(v['name'] for v in available)}"
        )
    if selected["backend"] == "releases" and not selected["ref"]:
        raise CLIError(f"Version {name} has no STABLE_COMMIT for this branch's fetcher")
    return name


def image_name(args, version):
    return (
        args.image
        or f"magma-cli/{RELEASE}/{args.fuzzer}/{args.target}:{version.lower()}"
    )


def listing(args):
    if args.entity == "fuzzers":
        return [
            {
                "name": f,
                "source_coverage": (ROOT / "fuzzers" / f / "coverage.sh").is_file(),
            }
            for f in names("fuzzers", "run.sh")
        ]
    if args.entity == "targets":
        return [
            {"name": t, "programs": list(programs(t)), "versions": versions(t)}
            for t in names("targets", "configrc")
        ]
    if not args.target:
        raise CLIError(f"list {args.entity} requires --target")
    directory = target_dir(args.target)
    if args.entity == "programs":
        return [
            {"name": name, "args": argv} for name, argv in programs(args.target).items()
        ]
    if args.entity == "versions":
        return versions(args.target)
    return [p.stem for p in sorted((directory / "patches" / "bugs").glob("*.patch"))]


def mount(path, destination, readonly=False):
    if ":" in str(path):
        raise CLIError(f"Docker bind mount paths cannot contain ':': {path}")
    return ["--volume", f"{path}:{destination}" + (":ro" if readonly else "")]


def inputs(paths):
    result = []
    for path in paths:
        path = path.expanduser().resolve()
        if path.is_file():
            result.append(path)
        elif path.is_dir():
            result.extend(p.resolve() for p in sorted(path.rglob("*")) if p.is_file())
        else:
            raise CLIError(f"Input does not exist or is not a file/directory: {path}")
    if not result:
        raise CLIError("No input files found")
    return list(dict.fromkeys(result))


# Fixed container paths keep filenames and CLI values out of shell source.
REPLAY_SCRIPT = """set -eu
cd "$SHARED"
cp /magma_input/testcase "$SHARED/testcase"
unset SOURCE_COVERAGE
exec "$OUT/monitor" --fetch watch --dump human /bin/bash -c 'exec "$FUZZER/runonce.sh" "$1" >&2' replay "$SHARED/testcase"
"""


def plan(args):
    if args.fuzzer not in names("fuzzers", "run.sh"):
        raise CLIError(f"Unknown fuzzer: {args.fuzzer}; use list fuzzers")
    version = selected_version(args)
    image = image_name(args, version)
    if not image or image.startswith("-") or any(c.isspace() for c in image):
        raise CLIError("Invalid image name")
    data = {
        "image": image,
        "target_version": version,
        "fuzzer": args.fuzzer,
        "target": args.target,
    }
    if args.command == "build":
        if (
            args.source_coverage
            and not (ROOT / "fuzzers" / args.fuzzer / "coverage.sh").is_file()
        ):
            raise CLIError(f"{args.fuzzer} has no source coverage replay support")
        cmd = [
            "docker",
            "build",
            "--tag",
            image,
            "--file",
            str(ROOT / "docker" / "Dockerfile"),
        ]
        build_args = {
            "fuzzer_name": args.fuzzer,
            "target_name": args.target,
            "USER_ID": os.getuid() or 1000,
            "GROUP_ID": os.getgid() or 1000,
        }
        if version != "FIXED":
            build_args["target_version"] = version
        if args.canary_mode != "plain":
            build_args["canaries" if args.canary_mode == "canaries" else "fixes"] = 1
        for attr, key in (
            ("isan", "isan"),
            ("harden", "harden"),
            ("source_coverage", "source_coverage"),
        ):
            if getattr(args, attr):
                build_args[key] = 1
        for key, value in build_args.items():
            cmd += ["--build-arg", f"{key}={value}"]
        for key, value in {
            "release": RELEASE,
            "fuzzer": args.fuzzer,
            "target": args.target,
            "target-version": version,
            "canary-mode": args.canary_mode,
        }.items():
            cmd += ["--label", f"org.magma.cli.{key}={value}"]
        if args.no_cache:
            cmd += ["--no-cache"]
        cmd.append(str(ROOT))
        data["commands"] = [cmd]
        return data
    program_args = programs(args.target)
    if args.program not in program_args:
        raise CLIError(
            f"Unknown program: {args.program}; available: {', '.join(program_args)}"
        )
    data["program"] = args.program
    name = "magma-cli-" + uuid.uuid4().hex[:12]
    data["container_name"] = name
    cmd = [
        "docker",
        "run",
        "--rm",
        "--init",
        "--name",
        name,
        "--network=none",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "--env",
        f"PROGRAM={args.program}",
        "--env",
        f"ARGS={program_args[args.program] if args.args is None else args.args}",
    ]
    if args.command == "run":
        workdir = args.workdir.expanduser().resolve()
        if workdir.exists() and (not workdir.is_dir() or any(workdir.iterdir())):
            raise CLIError(f"Workdir must be new or empty: {workdir}")
        if args.affinity:
            if not re.fullmatch(r"\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*", args.affinity):
                raise CLIError("Invalid CPU affinity; use 0,2-3")
            cmd += [
                "--cpuset-cpus",
                args.affinity,
                "--env",
                f"AFFINITY={args.affinity}",
            ]
        cmd += mount(workdir, "/magma_shared")
        cmd += [
            "--cap-add=SYS_PTRACE",
            "--security-opt",
            "seccomp=unconfined",
            "--env",
            f"TIMEOUT={args.timeout}",
            "--env",
            f"POLL={args.poll}",
            "--env",
            f"FUZZARGS={args.fuzz_args}",
            "--entrypoint",
            "/bin/bash",
            image,
            "-c",
            'exec "$MAGMA/run.sh" "$TARGET/corpus/$PROGRAM"',
        ]
        data.update(workdir=str(workdir), commands=[cmd])
    else:
        if args.expect_bug and not re.fullmatch(r"[A-Za-z0-9_]+", args.expect_bug):
            raise CLIError("Invalid expected bug ID")
        files = inputs(args.input)
        cmd += [
            "--tmpfs",
            f"/magma_shared:exec,uid={os.getuid()},gid={os.getgid()},mode=0700",
        ]
        data["inputs"] = [str(p) for p in files]
        data["commands"] = [
            cmd
            + mount(p, "/magma_input/testcase", True)
            + ["--entrypoint", "/bin/bash", image, "-c", REPLAY_SCRIPT]
            for p in files
        ]
    return data


def inspect_image(args, data):
    result = subprocess.run(
        ["docker", "image", "inspect", data["image"]],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode:
        raise CLIError(
            f"Cannot inspect image {data['image']}; build it first. {result.stderr.strip()}",
            1,
        )
    config = json.loads(result.stdout)[0]["Config"]
    labels = config.get("Labels") or {}
    expected = {
        "release": RELEASE,
        "fuzzer": args.fuzzer,
        "target": args.target,
        "target-version": data["target_version"],
    }
    for key, value in expected.items():
        actual = labels.get("org.magma.cli." + key)
        if actual is not None and actual != value:
            raise CLIError(
                f"Image {key} is {actual}, requested {value}; build/select the matching image",
                1,
            )
    env = dict(item.split("=", 1) for item in config.get("Env", []) if "=" in item)
    for key, expected_name in (("FUZZER", args.fuzzer), ("TARGET", args.target)):
        if Path(env.get(key, "")).name != expected_name:
            raise CLIError(f"Image {key} does not match {expected_name}", 1)
    if args.command == "replay" and args.expect_bug:
        mode = labels.get("org.magma.cli.canary-mode")
        if (mode is not None and mode != "canaries") or (
            "CFLAGS" in env and "-DMAGMA_ENABLE_CANARIES" not in env["CFLAGS"]
        ):
            raise CLIError(
                "--expect-bug requires an image built with --canary-mode canaries", 1
            )
    return env


def remove_container(name):
    try:
        subprocess.run(
            ["docker", "rm", "--force", name],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        pass


def execute(cmd, log, capture=False, timeout=None):
    """Stream diagnostics to stderr; capture oracle output separately for replay."""
    with (
        tempfile.TemporaryFile(mode="w+", errors="replace") as diagnostics,
        subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=diagnostics if capture else subprocess.STDOUT,
            text=True,
            errors="replace",
            start_new_session=True,
        ) as process,
    ):
        try:
            if capture:
                output, _ = process.communicate(timeout=timeout)
                diagnostics.seek(0)
                errors = diagnostics.read()
                sys.stderr.write(errors)
                if log:
                    log.write(errors)
                    log.write(output)
                return process.returncode, output
            for line in process.stdout:
                sys.stderr.write(line)
                if log:
                    log.write(line)
                    log.flush()
            return process.wait(), ""
        except BaseException:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            raise


def perform(args, data):
    if args.command != "build":
        inspect_image(args, data)
    if args.command == "run":
        Path(data["workdir"]).mkdir(parents=True, exist_ok=True)
    log_path = args.log_file.expanduser().resolve() if args.log_file else None
    if args.command == "run" and log_path is None:
        log_path = Path(data["workdir"]) / "cli.log"
    if log_path:
        # Refuse to overwrite an input, source file or a previous operation's log.
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log = log_path.open("x")
        data["log_file"] = str(log_path)
    else:
        log = None
    try:
        if args.command != "replay":
            code, _ = execute(data["commands"][0], log)
            return {
                **data,
                "status": "completed" if code == 0 else "failed",
                "process_exit_code": code,
            }, 0 if code == 0 else 1
        results = []
        for path, cmd in zip(data["inputs"], data["commands"]):
            try:
                code, output = execute(
                    cmd, log, capture=True, timeout=seconds(args.timeout)
                )
            except subprocess.TimeoutExpired:
                remove_container(data["container_name"])
                results.append(
                    {
                        "input": path,
                        "status": "timeout",
                        "process_exit_code": 124,
                        "triggered_bugs": [],
                        "bugs": [],
                    }
                )
                continue
            bugs = [
                {"id": m[0], "reached": int(m[1]), "triggered": int(m[2])}
                for m in re.findall(
                    r"^([A-Za-z0-9_]+) reached (\d+) triggered (\d+)$",
                    output,
                    re.MULTILINE,
                )
            ]
            triggered = sorted({b["id"] for b in bugs if b["triggered"]})
            # The fuzzer wrapper can return 1 for a crashing input. A confirmed
            # oracle trigger is a successful replay, not a Docker failure.
            status = (
                "triggered"
                if triggered and code in (0, 1)
                else "clean"
                if code == 0
                else "failed"
            )
            if (
                args.expect_bug
                and status in ("clean", "triggered")
                and args.expect_bug not in triggered
            ):
                status = "expectation_failed"
            results.append(
                {
                    "input": path,
                    "status": status,
                    "process_exit_code": code,
                    "triggered_bugs": triggered,
                    "bugs": bugs,
                }
            )
        failed = any(r["status"] in ("failed", "timeout") for r in results)
        missed = any(r["status"] == "expectation_failed" for r in results)
        code = 1 if failed else 3 if missed else 0
        return {
            **data,
            "status": "completed" if code == 0 else "failed",
            "results": results,
        }, code
    finally:
        if log:
            log.close()
        if args.command != "build":
            remove_container(data["container_name"])


def interrupt(signum, frame):
    raise KeyboardInterrupt


def main(argv=None):
    previous_handler = signal.signal(signal.SIGTERM, interrupt)
    command = None
    try:
        args = parser().parse_args(argv)
        command = args.command
        if command == "list":
            data, code = (
                {"status": "completed", "entity": args.entity, "items": listing(args)},
                0,
            )
        else:
            data = plan(args)
            if args.dry_run:
                data, code = {**data, "status": "planned", "cwd": str(ROOT)}, 0
            else:
                data, code = perform(args, data)
                data.pop("commands", None)
    except CLIError as exc:
        data, code = {"status": "error", "error": str(exc)}, exc.code
    except KeyboardInterrupt:
        data, code = {"status": "cancelled", "error": "Interrupted"}, 130
    except (OSError, subprocess.SubprocessError, ValueError, KeyError) as exc:
        data, code = {"status": "error", "error": str(exc)}, 1
    finally:
        signal.signal(signal.SIGTERM, previous_handler)
    print(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "release": RELEASE,
                "command": command,
                **data,
                "exit_code": code,
            },
            indent=2,
        )
    )
    return code
