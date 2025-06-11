import os
import argparse
import subprocess
import json
from datetime import datetime

def get_timestamp(filepath):
    return os.path.getmtime(filepath)

def merge_profdata_to_profraw(corpus_dir, profdata_path, timestamp):
    """
    Given a single .profdata file, find all .profdata files in the same directory
    that have a timestamp <= current file, and merge them into a .profraw.
    """
    cov_dir = os.path.dirname(profdata_path)

    target_name = os.path.splitext(os.path.basename(profdata_path))[0]
    profraw_path = os.path.join(cov_dir, f"{target_name}.profraw")

    # Collect all profdata files up to current timestamp
    profdata_files = [
        os.path.join(cov_dir, f"{f}.profdata")
        for f in os.listdir(corpus_dir)
        if os.path.exists(os.path.join(cov_dir, f"{f}.profdata")) and os.path.getmtime(os.path.join(corpus_dir, f)) <= timestamp 
    ]
    assert(profdata_path in profdata_files)

    if not profdata_files:
        raise FileNotFoundError("No .profdata files found to merge.")

    cmd_merge = ["llvm-profdata", "merge", "-output", profraw_path] + profdata_files
    result = subprocess.run(cmd_merge, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"llvm-profdata merge failed:\n{result.stderr}")

    return profraw_path

def generate_json_report(profraw_path, binary_path, output_json_path):
    cmd_cov = [
        "llvm-cov", "export",
        "-format=text",
        "-summary-only",
        f"-instr-profile={profraw_path}",
        binary_path
    ]
    result_cov = subprocess.run(cmd_cov, capture_output=True, text=True)
    if result_cov.returncode != 0:
        raise RuntimeError(f"llvm-cov export failed:\n{result_cov.stderr}")

    with open(output_json_path, "w") as f:
        f.write(result_cov.stdout)

def parse_coverage_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    totals = data.get("data", [{}])[0].get("totals", {})
    branches = totals.get("branches", {})
    covered = branches.get("covered", 0)
    percent = branches.get("percent", 0.0)
    return covered, percent

def main(corpus_dir, profdata_dir, binary_path, output_txt, interval):
    results = []
    last_sampled_time = 0

    file_infos = []
    for root, _, files in os.walk(profdata_dir):
        for file in sorted(files):
            if file.endswith(".profdata"):
                profdata_path = os.path.join(root, file)
                testcase_path = os.path.join(corpus_dir, os.path.splitext(file)[0])
                timestamp = get_timestamp(testcase_path)
                file_infos.append((profdata_path, timestamp))

    file_infos.sort(key=lambda x: x[1])
    for profdata_path, timestamp in file_infos:
        try:
            # skip a few and always include the last one
            if timestamp - last_sampled_time >= interval or timestamp == file_infos[-1][1]:
                json_output = os.path.splitext(profdata_path)[0] + ".json"
                profraw_path = merge_profdata_to_profraw(corpus_dir, profdata_path, timestamp);
                generate_json_report(profraw_path, binary_path, json_output)
                covered, percent = parse_coverage_from_json(json_output)
                results.append((timestamp, covered, round(percent, 2)))
                last_sampled_time = timestamp
        except Exception as e:
            print(f"Error processing {profdata_path}: {e}")

    if len(results) == 0:
        return
    with open(output_txt, "w") as out:
        out.write(f"timestamp,covered,percent\n")
        for ts, covered, pct in sorted(results, key=lambda x: x[0]):
            out.write(f"{ts},{covered},{pct}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate coverage summary from .profdata files.")
    parser.add_argument("corpus_dir", help="Directory containing test cases")
    parser.add_argument("profdata_dir", help="Directory containing .profdata files")
    parser.add_argument("binary_path", help="Path to the instrumented binary")
    parser.add_argument("interval", help="Sample every `interval` seconds", type=int)
    parser.add_argument("--output", default="coverage_overtime.txt", help="Output summary .txt file")

    args = parser.parse_args()
    main(args.corpus_dir, args.profdata_dir, args.binary_path, args.output, args.interval)
