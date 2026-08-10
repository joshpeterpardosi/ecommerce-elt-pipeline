import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

from load import load_csv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
FIXTURE = Path(__file__).parent / "fixtures" / "sample_orders.csv"
TEST_TABLE = "raw._test_load_csv_orders"


def test_load_csv_creates_table_matching_source_row_count_and_schema():
    client = bigquery.Client(project=PROJECT)
    client.delete_table(f"{PROJECT}.{TEST_TABLE}", not_found_ok=True)

    try:
        load_csv(csv_path=FIXTURE, table_id=TEST_TABLE, project=PROJECT)

        table = client.get_table(f"{PROJECT}.{TEST_TABLE}")

        assert table.num_rows == 3
        assert {field.name for field in table.schema} == {
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        }
    finally:
        client.delete_table(f"{PROJECT}.{TEST_TABLE}", not_found_ok=True)
