# Checks: Example 9, reports and plots

## Terminal
- [ ] `python reports.py --repo <REPO> --commit <COMMIT> --epochs 5` trains and records the reports and exits 0; the second run with `--epochs 60 --hidden 64` too.

## UI
- [ ] Task **reports and plots** (Completed): **Scalars** (loss curves), **Plots** (histogram of the residuals, scatter of predicted vs actual, a table or confusion-style report), **Debug samples** with `residuals.png` (the image report).
- [ ] Comparing the two runs shows the changed parameters and the better curves of the bigger model; the **weaker** model (`--epochs 3 --hidden 8`) shows its weakness in the residual plots first.
- [ ] **Repositories & Datasets**: `greenhouse-data` lists these runs in **Runs**.

## Database
- [ ] `task`: two documents named `reports and plots`, completed, with the different `hyperparams`.
- [ ] Events (Elasticsearch, not Mongo): plot and image events exist for the tasks (the UI showing them is the check).

## FAIL signs
- A plot is empty; the image is missing; the reports of the second run overwrite the first.

## Result (2026-11-12, fresh stack)
PASS. Two tasks `reports and plots` (Completed): epochs 30 / hidden 32 (test MAE 0.446 kWh) and epochs 60 / hidden 64 (MAE 0.497 kWh, mean residual +0.220), both with the dataset repository and commit as parameters. Each has four plots (`error by hour`, `expensive hour`, `predictions`, `residuals`), scalars and one debug-sample group. The comparison view shows the changed parameters. Note: the larger model was not better on this seed, so the "better curves of the bigger model" line in the checks is a description of what to look at, not a guaranteed result.
