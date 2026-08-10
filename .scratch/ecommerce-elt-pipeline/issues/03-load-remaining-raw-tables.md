# 03 — Load remaining raw tables

**What to build:** All 8 remaining Olist CSVs (Customers, Order Items, Payments, Reviews, Products, Sellers, Geolocation, Category Translation) landed in raw BigQuery tables, following the loader pattern proven in ticket 02.

**Blocked by:** 02.

**Status:** ready-for-agent

- [ ] Loader script extended to load all remaining raw CSVs into BigQuery
- [ ] Each raw table has an integration test asserting row count and schema against its source CSV
- [ ] All 9 raw tables (including Orders from ticket 02) queryable in BigQuery
