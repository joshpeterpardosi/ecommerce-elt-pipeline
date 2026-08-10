import argparse
import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

RAW_TABLE_MAP = {
    "olist_orders_dataset.csv": "orders",
    "olist_customers_dataset.csv": "customers",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_name_translation",
}


def load_csv(csv_path: Path, table_id: str, project: str) -> bigquery.LoadJob:
    client = bigquery.Client(project=project)

    with open(csv_path, encoding="utf-8-sig", newline="") as header_file:
        header = next(csv.reader(header_file))
    schema = [bigquery.SchemaField(name, "STRING") for name in header]

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=schema,
        allow_quoted_newlines=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(
            source_file, f"{project}.{table_id}", job_config=job_config
        )
    return job.result()


def load_all(raw_data_dir: Path, project: str, dataset: str = "raw") -> None:
    for csv_name, table_name in RAW_TABLE_MAP.items():
        result = load_csv(raw_data_dir / csv_name, f"{dataset}.{table_name}", project)
        print(f"loaded {result.output_rows} rows into {dataset}.{table_name}")


if __name__ == "__main__":
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    project = os.environ["GOOGLE_CLOUD_PROJECT"]

    parser = argparse.ArgumentParser(description="Load Olist CSVs into raw BigQuery tables.")
    parser.add_argument("csv_path", type=Path, help="a single CSV, or a directory to load all raw CSVs from")
    parser.add_argument("table_id", nargs="?", help="dataset.table, e.g. raw.orders (omit when csv_path is a directory)")
    args = parser.parse_args()

    if args.csv_path.is_dir():
        load_all(args.csv_path, project)
    else:
        result = load_csv(args.csv_path, args.table_id, project)
        print(f"loaded {result.output_rows} rows into {args.table_id}")
