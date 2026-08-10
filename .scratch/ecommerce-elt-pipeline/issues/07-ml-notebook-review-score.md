# 07 — ML notebook: Review Score prediction

**What to build:** A notebook that trains and evaluates a model predicting Review Score from the Review Prediction mart, closing the raw-data-to-model story of the project.

**Blocked by:** 06.

**Status:** ready-for-agent

- [ ] Notebook reads the Review Prediction mart directly from BigQuery (no separate feature pipeline)
- [ ] Model trained (classifier or regressor, per chosen framing) on a held-out train/test split
- [ ] Evaluation metrics (accuracy/F1 or RMSE) reported for the held-out split
- [ ] Notebook lives under `notebooks/` in the repo
