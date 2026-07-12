from types import SimpleNamespace

import pandas as pd

from src import data_loader


def test_loader_removes_only_fully_empty_rows(monkeypatch, tmp_path) -> None:
    source = pd.DataFrame(
        {
            "MotherEducation": [1.0, None, None],
            "Age": [14.0, 15.0, None],
        }
    )
    metadata = SimpleNamespace(
        column_names_to_labels={},
        variable_value_labels={},
        column_names=list(source.columns),
        number_rows=3,
        number_columns=2,
    )
    monkeypatch.setattr(data_loader.pyreadstat, "read_sav", lambda _: (source, metadata))
    path = tmp_path / "test.sav"
    path.touch()

    loaded, details = data_loader.load_spss_file(str(path))

    assert len(loaded) == 2
    assert pd.isna(loaded.loc[1, "MotherEducation"])
    assert details["filtered_rows"] == 1
    assert details["filter_method"] == "all_columns_missing"
