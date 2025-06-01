import os
import json
import tarfile
import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT_DIR = "captain/workdir_report_2025/ar"
CACHE_PATH = "coverage_data.pkl"

records = []

def load_cov_data():
    # Step 1: Load data into DataFrame
    for root, dirs, files in os.walk(ROOT_DIR):
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
        if "coverage-reports.json" in files:
            json_path = os.path.join(root, "coverage-reports.json")
            html_path = os.path.join(root, "coverage-reports/index.html")
            parts = os.path.normpath(json_path).split(os.sep)
            try:
                fuzzer, target, program, run = parts[-5:-1]
            except ValueError:
                continue  # skip non-matching paths
            with open(json_path, "r") as f:
                try:
                    data = json.load(f)
                    totals = data["data"][0]["totals"]["branches"]
                    record = {
                        "fuzzer": fuzzer,
                        "target": target,
                        "program": program,
                        "run": run,
                        "percent": totals["percent"],
                        "covered": totals["covered"],
                        "count": totals["count"],
                        "html_path": html_path
                    }
                    records.append(record)
                except Exception as e:
                    print(f"Error parsing {json_path}: {e}")

    df = pd.DataFrame(records)
    return df

figures = []

def gen_figures(df: pd.DataFrame):
    for (target, program), group in df.groupby(["target", "program"]):
        # 1. Coverage Percentage Figure (Y = percent)
        plot_df = group[["fuzzer", "percent"]].dropna()
        fig_percent = px.box(
            plot_df,
            x="fuzzer",
            y="percent",
            points="all",
        )

        # 2. Covered Branches Figure (Y = covered)
        plot_df = group[["fuzzer", "covered"]].dropna()
        fig_covered = px.box(
            plot_df,
            x="fuzzer",
            y="covered",
            points="all",
        )

        # Collect both figures for display
        links = group.apply(
            lambda row: f'<a href="{row["html_path"]}">{row["fuzzer"]} / {row["run"]}</a>', axis=1
        ).tolist()

        figures.append({
            "key": f"{target}/{program}",
            "fig_percent": fig_percent.to_html(full_html=False, include_plotlyjs=True),
            "fig_covered": fig_covered.to_html(full_html=False, include_plotlyjs=True),
            "links": links
        })

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
        "<table>"
    ]

    for fig in figures:
        html_parts.append(f"<tr><td colspan='2'><h2>{fig['key']}</h2></td></tr>")
        html_parts.append("<tr>")
        html_parts.append(f"<td>{fig['fig_percent']}</td>")
        html_parts.append(f"<td>{fig['fig_covered']}</td>")
        html_parts.append("</tr>")
        html_parts.append("<tr><td colspan='2'><ul>")
        for link in fig["links"]:
            html_parts.append(f"<li>{link}</li>")
        html_parts.append("</ul></td></tr>")

    html_parts.append("</table></body></html>")

    with open("coverage_summary.html", "w") as f:
        f.write("\n".join(html_parts))
    print("HTML report generated.")

def gen_cov_report(df: pd.DataFrame):
    gen_figures(df)
    plot_figures()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML coverage report.")
    parser.add_argument("root_dir", help="Root directory containing coverage data")
    args = parser.parse_args()

    ROOT_DIR = args.root_dir

    if os.path.exists(CACHE_PATH):
        print("Loading cached DataFrame...")
        df = pd.read_pickle(CACHE_PATH)
    else:
        print("Scanning {ROOTD_RI} for coverage-reports.json ...")
        df = load_cov_data()
        df.to_pickle(CACHE_PATH)
        print("Saved DataFrame to cache.")
    
    gen_cov_report(df)

