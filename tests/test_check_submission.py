"""Tests for check_submission without lab images or a network."""

from pathlib import Path

import pytest

from check_submission import check_submission, summarize_mot_text


def _rows(frames: range, track_id: int) -> str:
    return "".join(f"{f},{track_id},0,0,10,20,0.9,-1,-1,-1\n" for f in frames)


def _lab_tree(root: Path, n_imgs: int = 20) -> None:
    for index in range(1, 6):
        img_dir = root / f"video_{index}" / "img1"
        img_dir.mkdir(parents=True, exist_ok=True)
        for frame in range(1, n_imgs + 1):
            (img_dir / f"{frame:06d}.jpg").write_bytes(b"")


def _submission(root: Path, last_frame: int = 20, skip: str = "") -> Path:
    out = root / "nop_bai"
    out.mkdir()
    for index in range(1, 6):
        name = f"video_{index}"
        if name != skip:
            (out / f"{name}.txt").write_text(_rows(range(1, last_frame + 1), 1) + _rows(range(1, 4), 2))
    return out


def test_summarize_counts_ids_and_short_tracks() -> None:
    stats = summarize_mot_text(_rows(range(1, 16), 1) + _rows(range(3, 6), 7) + "\n")
    assert stats == {"n_rows": 18, "max_frame": 15, "n_ids": 2, "n_short_ids": 1}


def test_summarize_empty_text() -> None:
    assert summarize_mot_text("") == {"n_rows": 0, "max_frame": 0, "n_ids": 0, "n_short_ids": 0}


def test_summarize_rejects_short_line() -> None:
    with pytest.raises(ValueError):
        summarize_mot_text("1,2,3\n")


def test_full_submission_passes(tmp_path: Path) -> None:
    _lab_tree(tmp_path)
    assert check_submission(tmp_path, _submission(tmp_path)) is True


def test_missing_file_fails(tmp_path: Path) -> None:
    _lab_tree(tmp_path)
    assert check_submission(tmp_path, _submission(tmp_path, skip="video_3")) is False


def test_truncated_run_fails(tmp_path: Path) -> None:
    _lab_tree(tmp_path)
    assert check_submission(tmp_path, _submission(tmp_path, last_frame=5)) is False
