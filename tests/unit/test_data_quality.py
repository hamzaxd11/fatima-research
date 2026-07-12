import pandas as pd

from src.data_quality import detect_invalid_values


def test_invalid_value_detection_supports_nonconsecutive_index() -> None:
    frame = pd.DataFrame({"value": [1, 9]}, index=[10, 20])

    result = detect_invalid_values(frame, {"value": {"valid_values": [1, 2]}})

    assert len(result) == 1
    assert result.iloc[0]["current_value"] == "9"
    assert result.iloc[0]["row_number"] == 21
