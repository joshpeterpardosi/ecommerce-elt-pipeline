# v1 ships without orchestration or CI; dbt Core + BigQuery + a Python loader script only

The pipeline's E+L step is a small Python script (pandas + `google-cloud-bigquery`) loading Olist CSVs into raw BigQuery tables; dbt Core (local) handles T. No Airflow/Dagster and no CI (GitHub Actions) in v1, even though "ELT pipeline" implies a fuller production stack. This is a deliberate staged buildout: the author is learning dbt and BigQuery for the first time, so v1 stays focused on modeling correctness (staging, marts, tests) before adding orchestration and CI as a v2 layer. Reject the assumption that a missing Airflow DAG means the pipeline is incomplete — it's sequenced, not skipped.

## Update — CI, partially superseded

The no-CI half of this decision no longer holds. `.github/workflows/ci.yml` now lints the loader, validates the dbt model graph with `dbt parse`, and checks that the loader tests import — all without warehouse credentials, which is what made the step cheap enough to take early.

The reasoning above still stands for the rest: `dbt build` and the loader tests need a service-account secret and a live BigQuery dataset, and orchestration is still unbuilt. Those remain v2.
