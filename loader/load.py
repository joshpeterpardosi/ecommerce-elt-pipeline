import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery


def load_csv(csv_path: Path, table_id: str, project: str) -> bigquery.LoadJob:
    client = bigquery.Client(project=project)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(
            source_file, f"{project}.{table_id}", job_config=job_config
        )
    return job.result()


if __name__ == "__main__":
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    parser = argparse.ArgumentParser(description="Load a CSV into a raw BigQuery table.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("table_id", help="dataset.table, e.g. raw.orders")
    args = parser.parse_args()

    result = load_csv(args.csv_path, args.table_id, os.environ["GOOGLE_CLOUD_PROJECT"])
    print(f"loaded {result.output_rows} rows into {args.table_id}")
