"""Generate corrected manuscript figures without modifying preserved output bundles."""

import sys
from pathlib import Path
import argparse

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.visualizations import (
    plot_score_boxplots,
    plot_score_distributions,
    plot_scatter_matrix,
    plot_scores_by_maternal_education,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate manuscript-specific figures from a scored dataset")
    parser.add_argument(
        "dataset_path",
        nargs="?",
        default=str(ROOT / "output" / "analysis_20260319_173428" / "scored_dataset.csv"),
        help="Path to scored_dataset.csv (defaults to latest refreshed output bundle)",
    )
    args = parser.parse_args()

    dataset_path = Path(args.dataset_path)
    figures_dir = ROOT / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(dataset_path)

    plot_score_distributions(df, str(figures_dir), filename="manuscript_score_distributions.png")
    plot_scores_by_maternal_education(df, str(figures_dir), filename="manuscript_scores_by_maternal_education.png")
    plot_score_boxplots(df, str(figures_dir), filename="manuscript_score_boxplots.png")
    plot_scatter_matrix(df, str(figures_dir), filename="manuscript_scatter_matrix.png")


if __name__ == "__main__":
    main()
