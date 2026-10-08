# Tracking lab — student repo

Two-hour lab. The detector is fixed (`yolo26n.pt`, image size 640, person class). Students choose a tracker and the detector `conf` / `iou`. Only `video_1` ships with labels. `video_2` through `video_5` are judged by eye.

Human docs (`README.md`, `HUONG_DAN.md`, the report template) stay in Vietnamese. Docstrings, comments, and script messages stay in Vietnamese.

## Layout

- `scripts/` — `check_data.py`, `run_tracking.py`, `evaluate_practice.py`, `check_submission.py`. Run them from the repo root.
- `tests/` — unit tests. No GPU, no lab images, no network. `pytest.ini` sets `pythonpath = scripts` and `testpaths = tests` (TrackEval is cloned into the repo root).
- `on_tap_metrics.ipynb` — metric quiz, then one YOLO frame when `LAB_DATA` is set.
- `colab_lab.ipynb` — whole lab on Colab. Installs `boxmot` with `--no-deps` (its `numpy==1.23.1` pin has no wheel for Colab's Python) and patches its `float(array)` calls for NumPy >= 2.4.
- `submission_template/` — report the group fills in.

## Rules

- Google-style docstrings: one-line summary, then `Args`, `Returns`, and `Raises` when they apply.
- Every new pure function needs a unit test under `tests/`.
- Do not name the source dataset in this repo, and do not add labels for `video_2`–`video_5`.
- Do not commit `lab_data/`, preview videos, or `*.pt` weights.
- `evaluate_practice.py` scores only `video_1.txt`.

## Commands

Conda env `cv_robotics_lab21` (`environment.yml`).

```bash
pytest
python scripts/check_data.py --lab-data-root "$LAB_DATA"
```
