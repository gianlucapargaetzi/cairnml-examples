# Checks: Example 9, reports and plots

## Terminal
- [ ] `python reports.py --repo <REPO> --commit <COMMIT> --epochs 5` trains and records the reports and exits 0; the second run with `--epochs 60 --hidden 64` too.

## UI
- [ ] Task **reports and plots** (Completed): **Scalars** (loss curves), **Plots** (histogram of the residuals, scatter of predicted vs actual, a table or confusion-style report), **Debug samples** with `residuals.png` (the image report).
- [ ] The **residuals** plot is a histogram, not a per-row bar chart: 20 bars whose heights are all >= 0 and add up to the number of test rows (the Console line `Test set: <n> rows`), the labels under the bars are numbers in kWh (bin centres, spaced by one bin width), and the tallest bar is within one bin width of 0 kWh for the default run. A per-row chart shows one bar per test row, with the row index on the x axis and heights that add up to far less than the row count.
- [ ] Comparing the two runs shows the changed parameters and the better curves of the bigger model; the **weaker** model (`--epochs 3 --hidden 8`) shows its weakness in the residual plots first.
- [ ] **Repositories & Datasets**: `greenhouse-data` lists these runs in **Runs**.

## Database
- [ ] `task`: two documents named `reports and plots`, completed, with the different `hyperparams`.
- [ ] Events (Elasticsearch, not Mongo): plot and image events exist for the tasks (the UI showing them is the check).

## FAIL signs
- A plot is empty; the image is missing; the reports of the second run overwrite the first.

## Result (2026-11-12, fresh stack)
PASS. Two tasks `reports and plots` (Completed): epochs 30 / hidden 32 (test MAE 0.446 kWh) and epochs 60 / hidden 64 (MAE 0.497 kWh, mean residual +0.220), both with the dataset repository and commit as parameters. Each has four plots (`error by hour`, `expensive hour`, `predictions`, `residuals`), scalars and one debug-sample group. The comparison view shows the changed parameters. Note: the larger model was not better on this seed, so the "better curves of the bigger model" line in the checks is a description of what to look at, not a guaranteed result.

## Result (2026-11-24, fresh stack, SDK 0.0.9 from main)
PASS for the residuals plot (cairnml-examples#26). Defaults (30 epochs, hidden 32), dataset `greenhouse-data` at `734ceea`: the **residuals** plot has 20 bars, heights all >= 0 and adding up to 500 (the `Test set: 500 rows` line), labels `-1.30` to `1.78` in steps of about 0.16 (bin centres between the smallest residual -1.377 and the largest 1.861), the tallest bar centred at 0.16 kWh (bin width 0.162), mean residual +0.105 kWh, standard deviation of the residuals 0.546 kWh. The weaker model (`--epochs 3 --hidden 8`) has 20 bars adding up to 500 with labels `-4.01` to `3.37`, mean residual +0.058 kWh and a larger standard deviation, 1.234 kWh, so its histogram is wider, as the README says. Before the change the same plot had 500 bars (x axis 0, 1, 2, ... the row index), heights adding up to 52.45 and a smallest height of -1.38.
