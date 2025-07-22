import os
import json
import tarfile
import argparse
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT_DIR = "captain/workdir_report_2025/ar"
OUT_FILE = "coverage.html"
CACHE_PATH = "final_coverage.pkl"
COVERAGE_OVERTIME_CACHE_PATH = "coverage_overtime.pkl"

records = []
records_overtime = []
figures = []


def load_cov_data(target_dirs: list):
    # Step 1: Load data into DataFrame
    for root, _, files in os.walk(ROOT_DIR):
        if "coverage-reports.json" not in files and "ball.tar" in files:
            tar_path = os.path.join(root, "ball.tar")
            try:
                with tarfile.open(tar_path) as tar:
                    tar.extractall(path=root)
                    print(f"Extracted ball.tar in {root}")
                files = os.listdir(root)  # refresh the file list after extraction
                if "coverage-reports.json" not in files:
                    print(f"Failed to obtain coverage reports of {root}")
            except Exception as e:
                print(f"Failed to extract {tar_path}: {e}")
        if "coverage-reports.json" in files or "coverage_overtime.txt" in files:
            try:
                parts = os.path.normpath(root).split(os.sep)
                fuzzer, target, program, run = parts[-4:]
            except ValueError:
                continue
        if "coverage-reports.json" in files:
            json_path = os.path.join(root, "coverage-reports.json")
            html_path = os.path.join(root, "coverage-reports/index.html")
            parts = os.path.normpath(json_path).split(os.sep)
            with open(json_path, "r") as f:
                try:
                    data = json.load(f)
                    totals = data["data"][0]["totals"]["branches"]
                    record = {
                        "fuzzer": "afl++" if fuzzer == "aflplusplus" else fuzzer,
                        "target": target,
                        "program": program,
                        "run": run,
                        "percent": totals["percent"],
                        "covered": totals["covered"],
                        "count": totals["count"],
                        "html_path": html_path,
                    }
                    if not len(target_dirs) or target in target_dirs:
                        records.append(record)
                except Exception as e:
                    print(f"Error parsing {json_path}: {e}")
        if "coverage_overtime.txt" in files:
            txt_path = os.path.join(root, "coverage_overtime.txt")
            try:
                df = pd.read_csv(txt_path)
                df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
                df["timestamp"] = pd.to_datetime(
                    df["timestamp"], unit="s", errors="coerce"
                )
                df = df.dropna(subset=["timestamp"])

                df["timestamp"] = df["timestamp"].dt.floor("s")
                df = df.drop_duplicates(subset="timestamp", keep="last")
                df = df.sort_values("timestamp").reset_index(drop=True)
                df = df.ffill()

                start_time = df["timestamp"].iloc[0]
                df["timestamp"] = (df["timestamp"] - start_time).dt.total_seconds()

                df["fuzzer"] = "afl++" if fuzzer == "aflplusplus" else fuzzer
                df["target"] = target
                df["program"] = program
                df["run"] = run
                if not len(target_dirs) or target in target_dirs:
                    records_overtime.append(df)
            except Exception as e:
                print(f"Failed to load {txt_path}: {e}")

    try:
        df = pd.DataFrame(records)
        df_overtime = pd.concat(records_overtime, ignore_index=True)
        return df, df_overtime
    except Exception as e:
        print(f"Error creating DataFrame: {e}. Is the target directory correct?")
        exit(1)


def get_overtime_stats(
    fuzzer_group: pd.DataFrame, time_grid: np.ndarray, stat_type: str
):
    interpolated_runs = []
    for _, run_group in fuzzer_group.groupby("run"):
        run_group = run_group.sort_values("timestamp")
        interp = np.interp(time_grid, run_group["timestamp"], run_group[stat_type])
        interpolated_runs.append(interp)

    interp_runs_arr = np.array(interpolated_runs)
    return {
        "median": np.median(interp_runs_arr, axis=0),
        "min": np.min(interp_runs_arr, axis=0),
        "max": np.max(interp_runs_arr, axis=0),
    }


def add_overtime_fuzzer_line(
    figure: go.Figure, time_grid: np.ndarray, stats: dict, fuzzer: str
):
    figure.add_trace(
        go.Scatter(
            x=time_grid,
            y=stats["median"],
            mode="markers" if len(time_grid) == 1 else "lines",
            name=f"{fuzzer} avg",
            line=dict(width=2),
        )
    )
    figure.add_trace(
        go.Scatter(
            x=np.concatenate([time_grid, time_grid[::-1]]),
            y=np.concatenate([stats["min"], stats["max"][::-1]]),
            fill="toself",
            fillcolor="rgba(0,100,200,0.1)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            name=f"{fuzzer} range",
            showlegend=False,
        )
    )


def gen_figures(df: pd.DataFrame, df_overtime: pd.DataFrame):
    for (target, program), group in df.groupby(["target", "program"]):
        # 1. Coverage Percentage Figure (Y = percent)
        plot_df = group[["fuzzer", "percent"]].dropna()
        fig_percent = px.box(plot_df, x="fuzzer", y="percent", points="all")

        # 2. Covered Branches Figure (Y = covered)
        plot_df = group[["fuzzer", "covered"]].dropna()
        fig_covered = px.box(plot_df, x="fuzzer", y="covered", points="all")

        df_overtime_program = df_overtime.query(
            "target == @target and program == @program"
        )
        time_grid = np.arange(0, df_overtime_program["timestamp"].max() + 1, 1)

        fig_percent_overtime = go.Figure()
        fig_covered_overtime = go.Figure()
        for fuzzer, fuzzer_group in df_overtime_program.groupby("fuzzer"):
            # 3. Coverage Overtime Figure (Y = percent)
            stats_p = get_overtime_stats(fuzzer_group, time_grid, "percent")
            add_overtime_fuzzer_line(fig_percent_overtime, time_grid, stats_p, fuzzer)

            # 4. Covered Branches Figure (Y = covered)
            stats_c = get_overtime_stats(fuzzer_group, time_grid, "covered")
            add_overtime_fuzzer_line(fig_covered_overtime, time_grid, stats_c, fuzzer)

        fig_percent_overtime.update_layout(xaxis_title="Time", yaxis_title="Percent")
        fig_covered_overtime.update_layout(xaxis_title="Time", yaxis_title="Covered")

        # Collect both figures for display
        links = group.apply(
            lambda row: f'<a href="{row["html_path"]}">{row["fuzzer"]} / {row["run"]}</a>',
            axis=1,
        ).tolist()

        figures.append(
            {
                "key": f"{target}/{program}",
                "fig_percent": fig_percent.to_html(
                    full_html=False, include_plotlyjs=True
                ),
                "fig_covered": fig_covered.to_html(
                    full_html=False, include_plotlyjs=True
                ),
                "fig_percent_overtime": fig_percent_overtime.to_html(
                    full_html=False, include_plotlyjs=True
                ),
                "fig_covered_overtime": fig_covered_overtime.to_html(
                    full_html=False, include_plotlyjs=True
                ),
                "links": links,
            }
        )


def plot_figures():
    html_parts = [
        "<html><head><title>Coverage Summary</title>",
        '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
        """
        <style>
            table {
                width: 100%;
                border-collapse: separate; /* keep cell spacing */
                border-spacing: 20px 15px; /* horizontal and vertical gaps */
                table-layout: fixed;       /* fix widths for consistent layout */
                font-family: Arial, sans-serif;
            }
            th, td {
                vertical-align: top;       /* align figures/text to top */
                padding: 8px;
                border: 1px solid #ddd;
                overflow: hidden;          /* prevent content overflow */
            }
            td {
                width: 50%;                /* each figure cell takes half width */
            }
            h2 {
                margin: 10px 0;
                font-size: 1.5em;
                text-align: left;
            }
            ul {
                margin: 0;
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
        </style>
        """,
        "</head><body>",
        "<h1>Coverage Summary</h1>",
        "<table>",
    ]

    for fig in figures:
        html_parts.append(f"<tr><td colspan='4'><h2>{fig['key']}</h2></td></tr>")
        html_parts.append("<tr>")
        html_parts.append(f"<td colspan='2'>{fig['fig_percent']}</td>")
        html_parts.append(f"<td colspan='2'>{fig['fig_covered']}</td>")
        html_parts.append("</tr><tr>")
        html_parts.append(f"<td colspan='2'>{fig['fig_percent_overtime']}</td>")
        html_parts.append(f"<td colspan='2'>{fig['fig_covered_overtime']}</td>")
        html_parts.append("</tr>")
        html_parts.append("<tr><td colspan='4'><ul>")
        for link in fig["links"]:
            html_parts.append(f"<li>{link}</li>")
        html_parts.append("</ul></td></tr>")

    html_parts.append("</table></body></html>")

    with open(OUT_FILE, "w") as f:
        f.write("\n".join(html_parts))
    print("HTML report generated.")


def gen_cov_report(df: pd.DataFrame, df_overtime: pd.DataFrame):
    gen_figures(df, df_overtime)
    plot_figures()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML coverage report.")
    parser.add_argument(
        "--root_dir", help="Root directory containing coverage data", default=ROOT_DIR
    )
    parser.add_argument("--out_file", help="Output HTML file name", default=OUT_FILE)
    parser.add_argument(
        "--target",
        help="Specify one or more targets (default=all)",
        nargs="+",
        default=[],
    )
    parser.add_argument(
        "--cache", help="Use cached data if available", action="store_true"
    )
    args = parser.parse_args()

    ROOT_DIR = args.root_dir
    OUT_FILE = args.out_file

    if args.cache and os.path.exists(CACHE_PATH):
        print("Loading cached DataFrame...")
        df = pd.read_pickle(CACHE_PATH)
        df_overtime = pd.read_pickle(COVERAGE_OVERTIME_CACHE_PATH)
    else:
        print(f"Scanning {ROOT_DIR} for coverage-reports.json ...")
        df, df_overtime = load_cov_data(args.target)
        df.to_pickle(CACHE_PATH)
        df_overtime.to_pickle(COVERAGE_OVERTIME_CACHE_PATH)
        print("Saved DataFrame to cache.")

    gen_cov_report(df, df_overtime)
