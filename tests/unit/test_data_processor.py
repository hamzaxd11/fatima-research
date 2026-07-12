import pandas as pd

from src.data_processor import calculate_knowledge_score
from src.data_quality import generate_data_quality_report


def test_menstruation_process_scores_physiological_response() -> None:
    data = pd.DataFrame(
        {
            "WhatDoYouThinkAboutThePrecessofMensturation": [1.0, 2.0, None],
        }
    )

    scored = calculate_knowledge_score(data)

    assert scored["knowledge_score"].tolist() == [1, 0, 0]


def test_data_quality_uses_spss_value_label_domains() -> None:
    data = pd.DataFrame({"MaternalOccupation": [1.0, 2.0, 3.0]})

    report = generate_data_quality_report(
        data,
        value_labels={"MaternalOccupation": {1.0: "Working", 2.0: "Non-working"}},
    )

    assert report["summary"]["invalid_value_count"] == 1
    assert report["invalid_values"]["current_value"].tolist() == ["3.0"]


def test_data_quality_accepts_string_value_label_domains() -> None:
    data = pd.DataFrame({"Category": ["A", "B", "C"]})

    report = generate_data_quality_report(
        data,
        value_labels={"Category": {"A": "Alpha", "B": "Beta"}},
    )

    assert report["summary"]["invalid_value_count"] == 1
    assert report["invalid_values"]["current_value"].tolist() == ["C"]


def test_custom_valid_values_take_precedence_over_metadata() -> None:
    data = pd.DataFrame({"Category": [1, 2]})

    report = generate_data_quality_report(
        data,
        validation_rules={"Category": {"valid_values": [1]}},
        value_labels={"Category": {1: "One", 2: "Two"}},
    )

    assert report["summary"]["invalid_value_count"] == 1
    assert report["invalid_values"]["current_value"].tolist() == ["2"]
