"""Tests for evaluate_practice helpers without TrackEval, lab images or a network."""

import subprocess
from pathlib import Path

import pytest

from evaluate_practice import parse_summary, summary_path, trackeval_command

_FAKE_TRACKEVAL = """\
import sys
import numpy as np

# Giống TrackEval: dùng alias np.float / np.int đã bị bỏ từ NumPy 1.24.
np.zeros(1, dtype=np.float)
np.array([], np.int)
out = sys.argv[sys.argv.index("--TRACKERS_FOLDER") + 1]
open(out + "/ok.txt", "w").write(" ".join(sys.argv[1:]))
"""


def test_parse_summary_reads_header_and_values() -> None:
    text = "HOTA DetA MOTA IDSW IDF1\n45.5 40 50.25 12 55\n"
    assert parse_summary(text) == {"HOTA": 45.5, "DetA": 40.0, "MOTA": 50.25, "IDSW": 12.0, "IDF1": 55.0}


@pytest.mark.parametrize("text", ["", "HOTA MOTA\n", "HOTA MOTA\n1.0\n"])
def test_parse_summary_rejects_malformed(text: str) -> None:
    with pytest.raises(ValueError):
        parse_summary(text)


def test_summary_path_layout(tmp_path: Path) -> None:
    path = summary_path(tmp_path, "nhom01_video1", "LAB", "train")
    assert path == tmp_path / "data" / "trackers" / "mot_challenge" / "LAB-train" / "nhom01_video1" / "pedestrian_summary.txt"


def test_trackeval_command_patches_numpy_in_child(tmp_path: Path) -> None:
    script = tmp_path / "scripts" / "run_mot_challenge.py"
    script.parent.mkdir()
    script.write_text(_FAKE_TRACKEVAL, encoding="utf-8")
    trackers = tmp_path / "data" / "trackers" / "mot_challenge"
    trackers.mkdir(parents=True)

    cmd = trackeval_command(tmp_path, "nhom01_video1", "LAB", "train")
    subprocess.run(cmd, check=True, capture_output=True)

    args = (trackers / "ok.txt").read_text().split()
    assert args[args.index("--SEQ_INFO") + 1] == "video_1"
    assert args[args.index("--TRACKERS_TO_EVAL") + 1] == "nhom01_video1"
