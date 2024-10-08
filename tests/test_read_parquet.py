import pytest
import pandas as pd
from src.backend import read_parquet_file

def test_read_parquet_file_returns_non_empty_dataframe():
    # Arrange
    year = 2024
    month = 1

    # Act
    result = read_parquet_file(year, month)

    # Assert
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
