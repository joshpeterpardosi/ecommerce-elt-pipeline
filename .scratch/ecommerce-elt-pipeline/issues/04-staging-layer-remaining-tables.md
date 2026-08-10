# 04 — Staging layer for remaining tables

**What to build:** dbt staging models for every raw table besides Orders, applying the cleaning/grain decisions fixed in the spec and ADRs.

**Blocked by:** 03.

**Status:** ready-for-agent

- [ ] `stg_customers`: keyed on `customer_unique_id`, not `customer_id` (ADR 0001)
- [ ] `stg_order_items`: aggregated to Order grain (total price, total freight, item count, distinct sellers)
- [ ] `stg_payments`: aggregated to Order grain (total payment value, payment type mix, max installments)
- [ ] `stg_products`: joined to `product_category_name_translation`, English category name exposed; unmatched categories pass through as null
- [ ] `stg_sellers`: clean base with renamed/cast columns
- [ ] `stg_geolocation`: deduplicated to one row per `geolocation_zip_code_prefix` (mean lat/lng)
- [ ] Schema tests (`not_null`, `unique` on grain key) pass on each staging model
