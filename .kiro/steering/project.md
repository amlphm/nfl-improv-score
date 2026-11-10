# NFL Improv Score — Project Steering

## What this project is

**NFL Improv Score** is an entry for the **NFL Big Data Bowl (NYU Edition)**.

The core idea: when a play breaks down — the pocket collapses, the primary read
is covered, the quarterback scrambles or extends the play — some receivers
consistently improvise their way into open space. The **Improv Score**
quantifies that skill: *who gets open when the play falls apart.*

## Goals

- Detect "broken play" / improvisation moments from player-tracking data.
- Measure receiver "openness" (separation, leverage, space created) during those
  moments.
- Combine these into an interpretable per-player **Improv Score**.
- Communicate results clearly with visualizations and a written report.

## Data

- Source: NFL Next Gen Stats player-tracking data provided for the Big Data Bowl.
- Raw competition files live in `data/raw/` and are **gitignored** — never commit
  them. Only `.gitkeep` placeholders are tracked so the folder structure persists.
- Derived data flows `raw/` → `interim/` → `processed/`.

## Repository layout

- `data/` — raw / interim / processed datasets (contents gitignored).
- `notebooks/` — exploratory analysis and prototyping.
- `src/data/` — data loading & preprocessing.
- `src/features/` — feature engineering (improv detection, openness metrics).
- `src/models/` — model training and the Improv Score computation.
- `src/visualization/` — plots, field animations, and report figures.
- `reports/figures/` — generated graphics.
- `tests/` — unit tests.

## Conventions

- Language: **Python**. Dependencies tracked in `requirements.txt`.
- Keep notebooks for exploration; promote stable logic into `src/` modules.
- Prefer `pandas`/`numpy` for data wrangling and `scikit-learn` for modeling.
- Use `pyarrow`/parquet for intermediate data where practical.
- Do not commit data files or secrets; respect `.gitignore`.
- Favor interpretable, well-documented features — the "Improv Score" should be
  explainable, not a black box.
