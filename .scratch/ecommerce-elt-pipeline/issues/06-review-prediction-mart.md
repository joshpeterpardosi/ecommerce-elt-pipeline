# 06 — Review Prediction mart

**What to build:** The single wide mart the ML notebook reads from — one row per Order with every feature and the label assembled.

**Blocked by:** 05.

**Status:** ready-for-agent

- [ ] One row per Order, joining `fct_orders`, `dim_customers`, `dim_products`, and Order Items/Payments aggregates
- [ ] Review Score included as the label column
- [ ] Delivery Delay, price, freight, category, and payment-behavior columns present as features
- [ ] `not_null`/`unique` test on Order grain key passes
