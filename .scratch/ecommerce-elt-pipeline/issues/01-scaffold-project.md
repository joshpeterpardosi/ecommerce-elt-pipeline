# 01 — Scaffold project

**What to build:** A working dbt + BigQuery + Python foundation that the rest of the pipeline builds on — no pipeline logic yet, just a provably-connected toolchain.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] dbt Core project initialized, configured against a BigQuery dataset on the free tier
- [ ] `dbt debug` passes (connection + credentials verified)
- [ ] Python environment set up for the loader script (dependencies: pandas, google-cloud-bigquery)
- [ ] Repo layout in place for: loader script, dbt project (staging/marts folders), notebooks, docs
- [ ] Raw BigQuery dataset created for the loader script to write into
