import csv
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from google.cloud import bigquery

from load import RAW_TABLE_MAP, load_csv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
RAW_DATA_DIR = Path(__file__).resolve().parent.parent / "raw_data"


def _csv_row_count_and_columns(csv_path: Path) -> tuple[int, set[str]]:
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        row_count = sum(1 for _ in reader)
    return row_count, set(header)


@pytest.mark.parametrize("csv_name,table_name", RAW_TABLE_MAP.items())
def test_raw_table_matches_source_csv_row_count_and_schema(csv_name, table_name):
    csv_path = RAW_DATA_DIR / csv_name
    expected_rows, expected_columns = _csv_row_count_and_columns(csv_path)

    load_csv(csv_path=csv_path, table_id=f"raw.{table_name}", project=PROJECT)

    client = bigquery.Client(project=PROJECT)
    table = client.get_table(f"{PROJECT}.raw.{table_name}")

    assert table.num_rows == expected_rows
    assert {field.name for field in table.schema} == expected_columns
