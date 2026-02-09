"""Results tools: list campaigns, get results, extract PoCs, generate JSON reports."""

import json
import os
import sys

from mcp.server.fastmcp import FastMCP

from ..core import paths
from ..core.task_manager import TaskType, task_manager


def register(mcp: FastMCP):
    @mcp.tool()
    async def magma_list_campaigns(
        workdir: str,
        fuzzer: str = "",
        target: str = "",
    ) -> str:
        """List completed or in-progress campaigns in a workdir.

        Args:
            workdir: Path to the captain workdir (contains ar/ subdirectory)
            fuzzer: Optional filter by fuzzer name
            target: Optional filter by target name
        """
        ar_dir = os.path.join(workdir, "ar")
        if not os.path.isdir(ar_dir):
            return json.dumps({"error": f"Archive directory not found: {ar_dir}"})

        campaigns = []
        for f_name in sorted(os.listdir(ar_dir)):
            if fuzzer and f_name != fuzzer:
                continue
            f_path = os.path.join(ar_dir, f_name)
            if not os.path.isdir(f_path):
                continue

            for t_name in sorted(os.listdir(f_path)):
                if target and t_name != target:
                    continue
                t_path = os.path.join(f_path, t_name)
                if not os.path.isdir(t_path):
                    continue

                for p_name in sorted(os.listdir(t_path)):
                    p_path = os.path.join(t_path, p_name)
                    if not os.path.isdir(p_path):
                        continue

                    for run_id in sorted(os.listdir(p_path)):
                        run_path = os.path.join(p_path, run_id)
                        if not os.path.isdir(run_path):
                            continue
                        if not run_id.isdigit():
                            continue

                        has_tarball = os.path.exists(os.path.join(run_path, "ball.tar"))
                        has_monitor = os.path.isdir(os.path.join(run_path, "monitor"))

                        campaigns.append({
                            "fuzzer": f_name,
                            "target": t_name,
                            "program": p_name,
                            "run_id": run_id,
                            "has_tarball": has_tarball,
                            "has_monitor": has_monitor,
                        })

        return json.dumps({"campaigns": campaigns, "total": len(campaigns)}, indent=2)

    @mcp.tool()
    async def magma_get_campaign_results(
        workdir: str,
        fuzzer: str,
        target: str,
        program: str,
        run_id: str,
    ) -> str:
        """Get per-bug reach/trigger timing data for a specific campaign run.

        Uses exp2json's monitor parsing logic to extract time-to-bug data.

        Args:
            workdir: Path to the captain workdir
            fuzzer: Fuzzer name
            target: Target name
            program: Program name
            run_id: Run identifier (integer string)
        """
        # Import exp2json functions directly
        benchd_path = str(paths.BENCHD_DIR)
        if benchd_path not in sys.path:
            sys.path.insert(0, benchd_path)

        try:
            from exp2json import (
                extract_monitor_dumps,
                generate_monitor_df,
                get_ttb_from_df,
            )
        except ImportError:
            return json.dumps({
                "error": "Could not import exp2json.py. Ensure tools/benchd/exp2json.py exists."
            })

        campaign_path = os.path.join(workdir, "ar", fuzzer, target, program, run_id)
        if not os.path.isdir(campaign_path):
            return json.dumps({"error": f"Campaign directory not found: {campaign_path}"})

        tarball = os.path.join(campaign_path, "ball.tar")
        monitor_dir = os.path.join(campaign_path, "monitor")

        import tempfile
        import shutil

        tmpdir = None
        try:
            if os.path.isfile(tarball):
                tmpdir = tempfile.mkdtemp(prefix="magma_results_")
                os.makedirs(os.path.join(tmpdir, "monitor"), exist_ok=True)
                extract_monitor_dumps(tarball, os.path.join(tmpdir, "monitor"))
                df = generate_monitor_df(os.path.join(tmpdir, "monitor"), campaign_path)
            elif os.path.isdir(monitor_dir):
                df = generate_monitor_df(monitor_dir, campaign_path)
            else:
                return json.dumps({
                    "error": "No tarball or monitor directory found for this campaign."
                })

            if df is None or df.empty:
                return json.dumps({
                    "fuzzer": fuzzer,
                    "target": target,
                    "program": program,
                    "run_id": run_id,
                    "bugs": [],
                    "note": "No monitor data available.",
                })

            reached, triggered = get_ttb_from_df(df)

            # Merge reached and triggered into per-bug entries
            all_bugs = set(list(reached.keys()) + list(triggered.keys()))
            bugs = []
            for bug in sorted(all_bugs):
                bugs.append({
                    "id": bug,
                    "first_reached_s": reached.get(bug),
                    "first_triggered_s": triggered.get(bug),
                })

            return json.dumps({
                "fuzzer": fuzzer,
                "target": target,
                "program": program,
                "run_id": run_id,
                "bugs": bugs,
                "duration_seconds": int(df.index[-1]) if len(df) > 0 else 0,
                "poll_count": len(df),
            }, indent=2)

        except Exception as e:
            return json.dumps({"error": f"Failed to parse campaign results: {e}"})
        finally:
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)

    @mcp.tool()
    async def magma_extract_pocs(
        fuzzer: str,
        target: str,
        program: str,
        shared_dir: str,
        poc_dir: str = "",
    ) -> str:
        """Extract proof-of-concept crash inputs from campaign findings. Async operation.

        Wraps tools/captain/extract.sh to replay crashes through runonce.sh
        and identify which bugs they trigger.

        Args:
            fuzzer: Fuzzer name
            target: Target name
            program: Program name
            shared_dir: Path to campaign shared directory (contains findings/)
            poc_dir: Where to save extracted PoCs. Auto-created if empty.
        """
        from ..core.config_parser import parse_configrc

        if not os.path.isdir(shared_dir):
            return json.dumps({"error": f"Shared directory not found: {shared_dir}"})

        if not poc_dir:
            poc_dir = os.path.join(os.path.dirname(shared_dir), "pocs")
        os.makedirs(poc_dir, exist_ok=True)

        try:
            config = parse_configrc(target)
        except Exception as e:
            return json.dumps({"error": f"Failed to parse configrc: {e}"})

        args = config["program_args"].get(program, "")

        env = {
            "FUZZER": fuzzer,
            "TARGET": target,
            "PROGRAM": program,
            "ARGS": args,
            "SHARED": shared_dir,
            "POCDIR": poc_dir,
            "MAGMA": str(paths.MAGMA_ROOT),
        }

        record = await task_manager.spawn(
            task_type=TaskType.EXTRACT,
            description=f"extract pocs {fuzzer}/{target}/{program}",
            cmd=["bash", str(paths.EXTRACT_SH)],
            env=env,
            cwd=str(paths.MAGMA_ROOT),
        )

        return json.dumps({
            "task_id": record.task_id,
            "poc_dir": poc_dir,
            "status": "started",
        })

    @mcp.tool()
    async def magma_generate_json(
        workdir: str,
        output_file: str = "",
        workers: int = 4,
    ) -> str:
        """Convert campaign results in a workdir to a JSON summary. Async operation.

        Wraps tools/benchd/exp2json.py to aggregate monitor data across all
        campaigns into a single JSON file with reach/trigger timing.

        Args:
            workdir: Path to the captain workdir
            output_file: Path for JSON output. Auto-generated if empty.
            workers: Number of parallel workers (default 4)
        """
        if not os.path.isdir(workdir):
            return json.dumps({"error": f"Workdir not found: {workdir}"})

        if not output_file:
            output_file = os.path.join(workdir, "results.json")

        exp2json = str(paths.BENCHD_DIR / "exp2json.py")
        if not os.path.isfile(exp2json):
            return json.dumps({"error": f"exp2json.py not found at {exp2json}"})

        record = await task_manager.spawn(
            task_type=TaskType.REPORT,
            description=f"generate json from {workdir}",
            cmd=[
                sys.executable, exp2json,
                "--workers", str(workers),
                workdir, output_file,
            ],
        )

        return json.dumps({
            "task_id": record.task_id,
            "output_file": output_file,
            "status": "started",
        })
