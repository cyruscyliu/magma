import asyncio
import os
import tarfile

import pytest

from mmcp.tools import results


def _write_snapshot(monitor_dir, ts, header, row):
    os.makedirs(monitor_dir, exist_ok=True)
    path = os.path.join(monitor_dir, str(ts))
    with open(path, "w") as f:
        f.write(header + "\n" + row + "\n")


def test_extract_monitor_from_tarball(tmp_path):
    src = tmp_path / "src"
    _write_snapshot(src / "monitor", 5, "PNG001_R,PNG001_T", "3,1")
    tarball = tmp_path / "ball.tar"
    with tarfile.open(tarball, "w") as tf:
        tf.add(src / "monitor" / "5", arcname="ar/x/monitor/5")
        tf.add(src / "monitor" / "5", arcname="other/5")

    out_dir = tmp_path / "out" / "monitor"
    os.makedirs(out_dir)
    count = results._extract_monitor_from_tarball(str(tarball), str(out_dir))
    assert count == 1
    assert (out_dir / "5").read_text().startswith("PNG001_R")


def test_read_monitor_rows(tmp_path):
    monitor = tmp_path / "monitor"
    _write_snapshot(monitor, 10, "PNG001_R,PNG001_T", "5,0")
    _write_snapshot(monitor, 20, "PNG001_R,PNG001_T", "9,2")
    (monitor / "notnum").write_text("x")

    rows = results._read_monitor_rows(str(monitor))
    assert [t for t, _ in rows] == [10, 20]
    assert rows[1][1] == {"PNG001_R": "9", "PNG001_T": "2"}


def test_parse_monitor_bugs(tmp_path):
    monitor = tmp_path / "monitor"
    _write_snapshot(monitor, 10, "PNG001_R,PNG001_T,PNG002_R", "5,0,1")
    _write_snapshot(monitor, 30, "PNG001_R,PNG001_T,PNG002_R", "9,4,3")

    bugs = results._parse_monitor_bugs(str(monitor))
    by_id = {b["id"]: b for b in bugs}
    assert by_id["PNG001"]["reached"] is True
    assert by_id["PNG001"]["triggered"] is True
    assert by_id["PNG001"]["time_to_first_reached_s"] == 10
    assert by_id["PNG001"]["time_to_first_triggered_s"] == 30
    assert by_id["PNG002"]["triggered"] is False
    assert by_id["PNG002"]["time_to_first_reached_s"] == 10


def test_parse_monitor_bugs_no_data(tmp_path):
    assert results._parse_monitor_bugs(str(tmp_path / "empty")) is None


def test_get_monitor_dir_prefers_directory(tmp_path):
    campaign = tmp_path / "campaign"
    _write_snapshot(campaign / "monitor", 1, "A_R", "1")
    monitor_dir, cleanup = results._get_monitor_dir(str(campaign))
    assert cleanup is None
    assert monitor_dir.endswith("monitor")


def test_get_monitor_dir_from_tarball(tmp_path):
    src = tmp_path / "src"
    _write_snapshot(src / "monitor", 7, "A_R,A_T", "2,1")
    campaign = tmp_path / "campaign"
    os.makedirs(campaign)
    with tarfile.open(campaign / "ball.tar", "w") as tf:
        tf.add(src / "monitor" / "7", arcname="x/monitor/7")

    monitor_dir, cleanup = results._get_monitor_dir(str(campaign))
    try:
        assert os.path.isdir(monitor_dir)
    finally:
        if cleanup:
            import shutil

            shutil.rmtree(cleanup, ignore_errors=True)


def test_get_monitor_dir_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        results._get_monitor_dir(str(tmp_path / "nothing"))


def test_parse_extract_output():
    text = (
        "/repo/a.png exit_code 0 bug PNG001\n"
        "/repo/b.png exit_code 1\n"
        "\n"
        "garbage line\n"
    )
    out = results._parse_extract_output(text)
    assert out["status"] == "completed"
    assert len(out["lines"]) == 1
    assert out["lines"][0] == {
        "file": "/repo/a.png",
        "bug_id": "PNG001",
        "exit_code": 0,
        "triggered": 1,
        "reached": 1,
    }
    assert out["unparsed_lines"] == ["/repo/b.png exit_code 1", "garbage line"]


def test_map_cases_to_bugs():
    bugs = [{"id": "PNG001"}, {"id": "PNG002"}]
    cases = [
        {"file": "a.png", "bug_id": "PNG001", "reached": 1, "triggered": 1},
        {"file": "b.png", "bug_id": "PNG001", "reached": 0, "triggered": 0},
    ]
    out = results._map_cases_to_bugs(bugs, cases)
    by_id = {b["id"]: b for b in out}
    assert by_id["PNG001"]["testcases_that_reached"] == ["a.png"]
    assert by_id["PNG001"]["testcases_that_triggered"] == ["a.png"]
    assert by_id["PNG002"]["cases"] == []


def test_save_result_to_disk(tmp_path):
    entry1 = {"task_id": "t1", "data": 1}
    entry2 = {"task_id": "t2", "data": 2}
    entry1b = {"task_id": "t1", "data": 10}

    asyncio.run(results._save_result_to_disk(str(tmp_path), "b1", entry1))
    asyncio.run(results._save_result_to_disk(str(tmp_path), "b1", entry2))
    asyncio.run(results._save_result_to_disk(str(tmp_path), "b1", entry1b))

    import json

    with open(tmp_path / "results.json") as f:
        data = json.load(f)
    assert data["batch_id"] == "b1"
    assert len(data["results"]) == 2
    assert data["results"][0] == entry1b
    assert not [p for p in tmp_path.iterdir() if p.suffix == ".tmp"]
