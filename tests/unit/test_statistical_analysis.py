import pytest
import pandas as pd

from src.statistical_analysis import _compute_epsilon_squared, perform_sensitivity_analyses


def test_kruskal_epsilon_squared_definition() -> None:
    assert _compute_epsilon_squared(10.1562, 120, 5) == pytest.approx(10.1562 / 119)


def test_sensitivity_analysis_handles_single_group() -> None:
    data = pd.DataFrame(
        {
            "MotherEducation": [1, 1, 1],
            "knowledge_score": [4, 4, 4],
            "practice_score": [5, 5, 5],
        }
    )

    results = perform_sensitivity_analyses(data)

    assert not (results["analysis"] == "Holm-adjusted primary outcome").any()


def test_sensitivity_analysis_reports_analyzed_sample_size() -> None:
    data = pd.DataFrame(
        {
            "MotherEducation": [1, 1, 2, 2, None],
            "knowledge_score": [1, 2, 3, 4, 5],
            "practice_score": [2, 3, 4, 5, 6],
        }
    )

    results = perform_sensitivity_analyses(data)
    primary = results[results["analysis"] == "Holm-adjusted primary outcome"]

    assert set(primary["n"]) == {4}


def test_sensitivity_analyses_export_expected_checks() -> None:
    data = pd.DataFrame(
        {
            "MotherEducation": [1, 1, 2, 2, 3, 3, 4, 4, 5],
            "Age": [12, 13, 13, 14, 14, 15, 15, 16, 17],
            "IncomePerMonth": [10, 20, 20, 30, 30, 40, 40, 50, 60],
            "knowledge_score": [3, 4, 4, 5, 5, 6, 6, 7, 8],
            "practice_score": [4, 4, 5, 5, 5, 6, 6, 6, 7],
            "WhatDoYouThinkAboutThePrecessofMensturation": [1, 2, 1, 2, 1, 2, 1, 2, 1],
        }
    )

    results = perform_sensitivity_analyses(data)

    assert len(results) == 13
    assert set(results.columns) == {
        "analysis",
        "variables",
        "statistic",
        "p_value",
        "effect_size",
        "n",
    }
    assert (results["analysis"] == "Kruskal-Wallis confounder check").any()
    assert (results["analysis"] == "Archived pathological-response scoring key").any()
    assert (results["analysis"] == "Holm-adjusted primary outcome").sum() == 2
