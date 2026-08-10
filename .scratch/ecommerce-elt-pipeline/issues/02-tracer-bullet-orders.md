# 02 — Tracer bullet: Orders end-to-end

**What to build:** The full raw-to-mart path proven on a single entity (Orders), establishing the pattern every later table/model follows.

**Blocked by:** 01.

**Status:** ready-for-agent

- [ ] Loader script loads the Orders CSV into a raw BigQuery table
- [ ] Integration test asserts the raw Orders table's row count and schema match the source CSV
- [ ] `stg_orders` dbt model: renamed/cast columns, one row per Order
- [ ] `fct_orders` mart: Delivery Delay computed (`order_delivered_customer_date - order_estimated_delivery_date`, null when undelivered)
- [ ] Schema tests (`not_null`, `unique` on `order_id`) pass on `fct_orders`
- [ ] End-to-end path (CSV → raw → staging → mart) verified by querying `fct_orders` in BigQuery
