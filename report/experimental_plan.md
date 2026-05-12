# Experimental Plan - WC2026 Prediction

## Target definition

- Target variable: match outcome for the home team.
- Classes: W (home win), D (draw), L (home loss).
- Scope: international official matches, 2010-2024, used to train and validate.

## Train/validation/test chronology

- Train: matches before 2022-01-01.
- Validation: 2022-01-01 to 2023-12-31.
- Test: 2024-01-01 onward.

## Temporal validation protocol

- Primary split: fixed chronological split (train/val/test) for transparency.
- Secondary split: TimeSeriesSplit with gap to reduce leakage in CV.
- No random shuffle at any stage.

## Metrics

- Primary: log-loss (multiclass).
- Secondary: Brier score, accuracy, calibration curve.
- Optional: multi-class ROC-AUC (OVR), confusion matrix.

## Calibration procedure

- Calibrate champion with isotonic regression (CalibratedClassifierCV).
- Calibration fitted on training folds only, never on test.
- Validation used to verify reliability before simulation.

## Champion selection rule

- Choose the model with minimum log-loss on validation.
- Tie-breaker: best Brier score and calibration curve stability.
- Final model evaluated once on test, no tuning on test.

## Robustness tests

- Remove FIFA ranking features and compare log-loss.
- Replace rolling form window size (n=6, n=10) to test sensitivity.
- Include friendlies with lower weight and compare performance.
- Train without squad aggregates (FBref) and compare.
- Alternative split dates (e.g., 2021-01-01 and 2023-01-01).

## Limits and methodological notes

- International matches differ from club performance intensity and tactical structure.
- Squad lists may be incomplete or outdated for 2026.
- Rankings are proxies and can lag short-term form.

## Threats to validity

- Data leakage: rankings and form must be strictly prior to match date.
- Coverage: FBref club stats may not map to all national team players.
- Squad instability: injuries and selection changes reduce feature validity.
- Cross-domain gap: club stats may not transfer perfectly to national teams.
- Ranking dependence: ranking noise can bias results.
- Simulation assumptions: fixed form and Elo at tournament start.
