# NFL Improv Score

**NFL Big Data Bowl — NYU Edition**

> Improv Score: who gets open when the play falls apart.

When a play breaks down — the pocket collapses, the primary read is covered, the
quarterback scrambles — some receivers have a knack for improvising their way
into open space. The **Improv Score** aims to quantify that skill using NFL
Next Gen Stats player-tracking data.

## Project Structure

```
nfl-improv-score/
├── data/
│   ├── raw/            # Original, immutable tracking & play data (gitignored)
│   ├── interim/        # Intermediate, transformed data (gitignored)
│   └── processed/      # Final datasets ready for modeling (gitignored)
├── notebooks/          # Exploratory analysis and prototyping
├── src/
│   ├── data/           # Data loading & preprocessing
│   ├── features/       # Feature engineering (improv detection, openness, etc.)
│   ├── models/         # Model training & the Improv Score itself
│   └── visualization/  # Plots, field animations, reports
├── reports/
│   └── figures/        # Generated graphics and figures
├── tests/              # Unit tests
└── .kiro/
    └── steering/       # Project context & conventions for Kiro
```

## Getting Started

1. Place the competition data in `data/raw/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Explore in `notebooks/` or run pipelines from `src/`.

## License

TBD
