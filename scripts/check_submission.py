#!/usr/bin/env python
"""Kiểm tra thư mục nộp bài có đủ video_1.txt … video_5.txt chạy đủ frame.

In thêm vài con số thô cho từng video (số ID, số ID sống rất ngắn). Đây không
phải metric — chỉ là gợi ý chỗ cần xem lại video, nhất là bốn video không nhãn.

Ví dụ:
    python scripts/check_submission.py \\
        --lab-data-root "$LAB_DATA" \\
        --submission-dir runs/nop_bai
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from check_data import VIDEOS

SHORT_TRACK_FRAMES = 10  # ID sống dưới số frame này thường là hộp giả hoặc mảnh track bị đứt
MIN_FRAME_COVERAGE = 0.9  # frame cuối có track phải tới ít nhất 90% độ dài video


def summarize_mot_text(text: str) -> dict[str, int]:
    """Tóm tắt nội dung một file kết quả dạng MOT do ``run_tracking.py`` ghi.

    Args:
        text: Mỗi dòng ``frame,id,x,y,w,h,conf,-1,-1,-1``.

    Returns:
        Dict gồm ``n_rows`` (số hộp), ``max_frame`` (frame cuối có hộp),
        ``n_ids`` (số ID khác nhau) và ``n_short_ids`` (số ID xuất hiện ít
        hơn ``SHORT_TRACK_FRAMES`` frame).

    Raises:
        ValueError: Khi một dòng có ít hơn sáu cột hoặc frame / ID không phải số.
    """
    frames_per_id: Counter[int] = Counter()
    max_frame = 0
    n_rows = 0
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        cols = line.split(",")
        if len(cols) < 6:
            raise ValueError(f"Dòng {line_no} chỉ có {len(cols)} cột, cần ít nhất 6")
        frame, track_id = int(float(cols[0])), int(float(cols[1]))
        frames_per_id[track_id] += 1
        max_frame = max(max_frame, frame)
        n_rows += 1
    return {
        "n_rows": n_rows,
        "max_frame": max_frame,
        "n_ids": len(frames_per_id),
        "n_short_ids": sum(1 for n in frames_per_id.values() if n < SHORT_TRACK_FRAMES),
    }


def check_submission(lab_data_root: Path, submission_dir: Path) -> bool:
    """In trạng thái từng file nộp và báo bộ bài nộp có đủ chưa.

    Args:
        lab_data_root: Thư mục lab_data giảng viên phát.
        submission_dir: Thư mục chứa ``video_N.txt``, ví dụ ``runs/nop_bai``.

    Returns:
        True nếu cả năm file tồn tại, có hộp, và chạy gần hết số frame của video.
    """
    all_ok = True
    for name in VIDEOS:
        n_imgs = len(list((lab_data_root / name / "img1").glob("*.jpg")))
        txt = submission_dir / f"{name}.txt"
        if not txt.exists():
            print(f"[THIẾU] {name}: không có {txt}")
            all_ok = False
            continue
        stats = summarize_mot_text(txt.read_text())
        problems = []
        if stats["n_rows"] == 0:
            problems.append("file rỗng")
        if n_imgs and stats["max_frame"] > n_imgs:
            problems.append(f"frame {stats['max_frame']} vượt quá {n_imgs} ảnh")
        if n_imgs and stats["max_frame"] < MIN_FRAME_COVERAGE * n_imgs:
            problems.append("có vẻ chạy với --max-frames, hãy chạy lại đủ frame")
        status = "OK   " if not problems else "LỖI  "
        all_ok &= not problems
        print(
            f"[{status}] {name}: frame cuối {stats['max_frame']:4d}/{n_imgs:4d}, "
            f"{stats['n_rows']:6d} hộp, {stats['n_ids']:4d} ID, "
            f"{stats['n_short_ids']:4d} ID sống < {SHORT_TRACK_FRAMES} frame"
            + (f"  — {'; '.join(problems)}" if problems else "")
        )
    print("\nĐủ 5 file nộp." if all_ok else "\nChưa đủ điều kiện nộp — xem các dòng LỖI / THIẾU.")
    return all_ok


def main() -> None:
    """Đọc tham số dòng lệnh và kiểm tra thư mục nộp bài."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lab-data-root", required=True, type=Path, help="Thư mục lab_data giảng viên phát")
    parser.add_argument("--submission-dir", default=Path("runs/nop_bai"), type=Path, help="Thư mục chứa video_N.txt")
    args = parser.parse_args()
    check_submission(args.lab_data_root, args.submission_dir)


if __name__ == "__main__":
    main()
