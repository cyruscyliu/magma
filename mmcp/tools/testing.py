"""Testing tools: run test inputs against targets in ephemeral containers."""

import asyncio
import json
import os
import re
import shutil
import tempfile

from mcp.server.fastmcp import FastMCP

from ..core import docker_utils, paths
from ..core.config_parser import parse_configrc


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_test_input(
        fuzzer: str,
        target: str,
        program: str,
        input_path: str,
    ) -> str:
        """Run a single test case in an ephemeral Docker container to check if any bugs are reached or triggered.

        Spins up a temporary container from the pre-built magma/{fuzzer}/{target} image,
        runs the input through runonce.sh, parses canary output, and tears down.

        Args:
            fuzzer: Fuzzer name (e.g. 'aflplusplus')
            target: Target name (e.g. 'libpng')
            program: Program name (e.g. 'libpng_read_fuzzer')
            input_path: Absolute path to the test case file on the host
        """
        if not os.path.isfile(input_path):
            return json.dumps({"error": f"Input file not found: {input_path}"})

        image_name = f"magma/{fuzzer}/{target}"
        if not docker_utils.image_exists(image_name):
            return json.dumps({"error": f"Docker image not found: {image_name}. Build it first."})

        # Validate program
        try:
            config = parse_configrc(target)
        except Exception as e:
            return json.dumps({"error": f"Failed to parse configrc: {e}"})

        if program not in config["programs"]:
            return json.dumps({
                "error": f"Unknown program '{program}'. Available: {config['programs']}"
            })

        args = config["program_args"].get(program, "")

        # Create a temp directory with the input file
        tmpdir = tempfile.mkdtemp(prefix="magma_test_")
        try:
            input_basename = os.path.basename(input_path)
            shutil.copy2(input_path, os.path.join(tmpdir, input_basename))

            # Run in ephemeral container:
            # 1. Mount the temp dir as /test_input
            # 2. Set PROGRAM and ARGS env vars
            # 3. Run runonce.sh with the test file
            cmd = [
                "docker", "run", "--rm",
                f"--volume={tmpdir}:/test_input:ro",
                "--cap-add=SYS_PTRACE",
                "--security-opt=seccomp=unconfined",
                f"--env=PROGRAM={program}",
                f"--env=ARGS={args}",
                "--entrypoint=bash",
                image_name,
                "-c",
                f"cp /test_input/{input_basename} /magma_shared/runonce_input && "
                f"$MAGMA/runonce.sh /magma_shared/runonce_input",
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            stdout_bytes, _ = await asyncio.wait_for(
                process.communicate(), timeout=60
            )
            output = stdout_bytes.decode("utf-8", errors="replace").strip()
            exit_code = process.returncode

            # Parse output: "exit_code N bug BUGID" or just "exit_code N"
            bug_triggered = None
            match = re.search(r"bug\s+(\S+)", output)
            if match:
                bug_triggered = match.group(1)

            return json.dumps({
                "exit_code": exit_code,
                "bug_triggered": bug_triggered,
                "output": output,
            }, indent=2)

        except asyncio.TimeoutError:
            return json.dumps({
                "error": "Test timed out after 60 seconds",
                "exit_code": -1,
                "bug_triggered": None,
                "output": "",
            })
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
