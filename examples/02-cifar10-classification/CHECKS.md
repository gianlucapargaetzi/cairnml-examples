# Checks: Example 2, CIFAR-10 classification

## Terminal
- [ ] `python train.py --epochs 3` downloads the data once, trains, prints the final accuracy and exits 0.

## UI
- [ ] Project **examples** lists **CIFAR-10 classification**. While it runs: **Running**, a progress bar with a percentage, moving without a percentage while the images load.
- [ ] After the run: **Completed**. **Scalars**: loss and accuracy for the training and the validation part, one point per epoch (3 points). **Artifacts**: the trained weights.
- [ ] **Configuration** lists the epochs and the other arguments.
- [ ] **Repositories & Datasets**: unchanged from Example 1 (the same Code record at most; nothing new for the downloaded data).

## Database
- [ ] `task`: a new document `CIFAR-10 classification`, `status` completed, `hyperparams` holding the arguments.
- [ ] `repository`: no new record (CIFAR-10 is downloaded by the script, it is not a registry or a dataset repository).

## FAIL signs
- Accuracy is 0.1 on both parts (it does not learn), or the run is Completed with no validation curve.

## Result (2026-11-12)
- PASS: `python train.py --epochs 3` completed; validation accuracy 0.74, one artifact (the weights), the arguments in `hyperparams.Args`; no new repository record (still only the examples checkout).
