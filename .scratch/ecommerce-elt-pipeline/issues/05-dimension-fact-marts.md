# 05 — Dimension/fact marts + tests

**What to build:** The mart layer's dimensions finalized, and `fct_orders` extended with the Order Items/Payments aggregates joined in, with full referential-integrity test coverage.

**Blocked by:** 04.

**Status:** ready-for-agent

- [ ] `dim_customers`: one row per `customer_unique_id`, with derived order count
- [ ] `dim_products`: one row per Product, translated category name and physical attributes
- [ ] `dim_sellers`: one row per Seller
- [ ] `fct_orders` extended with Order Items and Payments aggregates joined in at Order grain
- [ ] `relationships` tests pass between `fct_orders` and each dimension (Customers, Products via Order Items, Sellers via Order Items)
- [ ] `not_null`/`unique` tests pass on every mart's primary key
