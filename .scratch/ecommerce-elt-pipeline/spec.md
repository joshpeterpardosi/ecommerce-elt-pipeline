Status: ready-for-agent

# Ecommerce ELT Pipeline

## Problem Statement

The author is a student targeting a data scientist role, self-learning by building a portfolio project. They have no hands-on experience with dbt or BigQuery, and currently have no project that demonstrates the full path from raw, messy real-world data to a clean analytical dataset to a trained model — most student portfolios stop at "loaded a clean Kaggle CSV into pandas." Without a project that shows the ELT step, a reviewer (recruiter/hiring manager) can't tell whether the author can build and reason about the data layer a data scientist actually depends on, not just consume one.

## Solution

Build a self-contained ELT pipeline over the Olist Brazilian e-commerce public dataset: a Python loader script lands the raw CSVs in BigQuery, dbt Core transforms them into tested staging and mart models, and a companion notebook trains a model predicting Review Score from the resulting marts. The repo ships with a full README (architecture, setup, findings) so it reads clearly to an outside reviewer. Orchestration (Airflow) and CI are deliberately deferred to a v2 phase (see [0002-staged-buildout-no-orchestration-v1.md](../../docs/adr/0002-staged-buildout-no-orchestration-v1.md)) so v1 stays focused on getting the data modeling right while the author is still learning the tools.

## User Stories

1. As the author, I want a Python script that loads each Olist CSV into a raw BigQuery table, so that dbt has a stable, queryable source to build on.
2. As the author, I want the loader script covered by an integration test that asserts row counts and schema for a sample CSV, so that I know the E+L step is correct before trusting anything built on top of it.
3. As the author, I want dbt staging models for each of the 9 raw tables, so that column renaming, type-casting, and light cleaning happen in one consistent layer instead of being repeated across marts.
4. As the author, I want the Customer grain in every customer-level model to use `customer_unique_id`, so that repeat buyers aren't miscounted as new customers (per [0001-customer-grain-uses-unique-id.md](../../docs/adr/0001-customer-grain-uses-unique-id.md)).
5. As the author, I want a `product_category_name_translation` join applied in staging, so that downstream marts expose English category names instead of raw Portuguese values.
6. As the author, I want geolocation data aggregated to one row per zip-code prefix (average lat/lng) in staging, so that joins to Customer/Seller don't fan out on the raw table's duplicate rows.
7. As the author, I want an Orders mart at the Order grain with Delivery Delay computed (`order_delivered_customer_date - order_estimated_delivery_date`), so that lateness is a single reusable column instead of being recomputed downstream.
8. As the author, I want an Order Items mart aggregated to Order grain (total price, total freight, item count, distinct sellers), so that Order-level analysis doesn't need to re-join and re-aggregate line items every time.
9. As the author, I want a Payments mart aggregated to Order grain (total payment value, payment type mix, max installments), so that an Order's payment behavior is queryable in one row.
10. As the author, I want a Customers dimension mart keyed on `customer_unique_id` with derived order counts, so that customer-level features (repeat purchase behavior) are ready for the ML notebook without extra joins.
11. As the author, I want a Products dimension mart with translated category names and physical attributes, so that product-level features are available for the review-score model.
12. As the author, I want a Sellers dimension mart, so that seller-level performance (if explored later) has a clean base.
13. As the author, I want a wide Review Prediction mart joining Orders, Order Items, Payments, Customers, and Products into one row per Order with Review Score as the label, so that the ML notebook has a single feature table to read from.
14. As the author, I want dbt schema tests (`not_null`, `unique`, `relationships`) on primary/foreign keys across staging and mart models, so that broken joins or duplicate grains are caught before they reach the notebook.
15. As the author, I want dbt's built-in documentation (`dbt docs generate`) hosted on GitHub Pages, so that a reviewer can click through model lineage without cloning the repo.
16. As the author, I want a notebook that trains a classifier/regressor predicting Review Score from the Review Prediction mart (delivery delay, price, freight, category, payment behavior), so that the project demonstrates a full raw-data-to-model pipeline.
17. As the author, I want the notebook to report standard evaluation metrics (accuracy/F1 or RMSE depending on framing) on a held-out split, so that the model's performance claim is credible to a reviewer.
18. As the author, I want a full README (problem, architecture diagram, setup steps, dataset description, key findings from the notebook), so that a recruiter can understand the project's value without running any code.
19. As the author, I want the repo name kept as `ecommerce-elt-pipeline`, so that it stays accurate through the later v2 orchestration addition without a rename.
20. As the author, I want BigQuery and dbt Core configured to run entirely on the free tier, so that the project costs nothing to build or demo.

## Implementation Decisions

- **Loader script**: Python, using `pandas` + `google-cloud-bigquery`. One function per source CSV (or one parameterized function taking file path + target table name), writing to a `raw` BigQuery dataset. No orchestration tool wraps it in v1 — run manually via CLI.
- **dbt project**: dbt Core, run locally, targeting BigQuery via the `dbt-bigquery` adapter. Two-layer model structure: `staging` (1:1 with raw tables, renamed/cast columns, light cleaning) and `marts` (business-grain models listed in the user stories above).
- **Customer grain**: all customer-level staging/marts key on `customer_unique_id`, never the order-scoped `customer_id`. See ADR 0001.
- **Geolocation handling**: aggregated in staging to one row per `geolocation_zip_code_prefix` (mean lat/lng) before any join, since the raw table has no clean primary key.
- **Category translation**: `product_category_name_translation` joined in the Products staging model; unmatched/null categories pass through as null rather than being dropped.
- **Delivery Delay**: computed once, in the Orders mart, as `order_delivered_customer_date - order_estimated_delivery_date`. Null when `order_delivered_customer_date` is null (undelivered/canceled orders).
- **Review Prediction mart**: single wide table, one row per Order, joining Orders, aggregated Order Items, aggregated Payments, Customers, and Products. This is the only table the ML notebook reads from.
- **v1 scope boundary**: no Airflow/Dagster, no CI (GitHub Actions). See ADR 0002. These are explicitly v2 work, tracked separately, not part of this spec's tickets.
- **dbt docs hosting**: `dbt docs generate` output published to GitHub Pages as a polish step, not a blocker for the core pipeline/notebook being done.
- **ML notebook**: standard Python data-science stack (pandas, scikit-learn), lives in-repo (e.g. `notebooks/`), reads only from the Review Prediction mart via the BigQuery client — no separate feature-engineering pipeline outside dbt.

## Testing Decisions

- **What makes a good test here**: tests assert observable outcomes (row counts, schema, key uniqueness, join correctness) — not internal implementation of the loader script or dbt's internal execution mechanics.
- **Loader script** (the one code seam): integration test(s) that run the loader against a small sample CSV fixture and assert the resulting BigQuery table has the expected row count and column schema. This is the only place traditional TDD applies in this spec.
- **dbt models**: verified via dbt's built-in schema tests (`not_null`, `unique`, `relationships`) declared in each model's `.yml` — not custom test code. Coverage: primary keys on every mart, foreign key relationships between Orders/Order Items/Payments/Customers/Products, and `not_null` on any column used as a join key or ML feature.
- **ML notebook**: no automated test seam. Correctness is judged by reported evaluation metrics on a held-out split, reviewed manually — this is exploratory/model-evaluation work, not unit-testable behavior.
- **No prior art in this repo** (greenfield project) — tests should follow standard practice for the tool: pytest-style integration test for the Python loader, dbt-native YAML schema tests for models.

## Out of Scope

- Airflow/Dagster orchestration (v2).
- CI (GitHub Actions running dbt build/test on push) (v2).
- Any live/API data source — pipeline is batch-only over the static Olist CSV export.
- Analyses other than Review Score prediction (delivery/logistics deep-dive, RFM segmentation, sales forecasting) — noted as possible future extensions, not built here.
- Data quality issues in `order_reviews` (reported duplicate rows in some community write-ups) beyond what dbt's standard `unique`/`not_null` tests catch — no bespoke dedup logic beyond the geolocation and order-item/payment aggregation already specified.
- Deployment of the ML model (no serving/API layer) — notebook-only.

## Further Notes

- Full schema reference (all 9 Olist tables, keys, join graph, and known data quality quirks) was captured during grilling and should be treated as background context for whoever implements the staging layer — see the conversation history / CONTEXT.md for the resolved domain vocabulary (Customer, Order, Order Item, Seller, Delivery Delay, Review Score).
- `customer_id` vs `customer_unique_id` and the geolocation dedup are the two quirks most likely to trip up an implementer unfamiliar with this dataset — both are already captured as ADRs/decisions above, not left implicit.
- Timeline is open-ended; no external deadline constrains ticket sequencing.
