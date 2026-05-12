# Finalization Checklist - WC2026

## Data checklist

- Confirm international_results.csv covers 2010-2024.
- Confirm FIFA rankings are merged with prior dates only.
- Verify team name normalization and mapping consistency.
- Confirm schedule and groups have 48 teams and 12 groups.
- Verify missing values for key features are documented.

## Model checklist

- Confirm W/D/L labels are correctly defined.
- Verify feature list matches training artifacts.
- Check models are saved to data/processed/models.
- Ensure no leakage variables (future outcomes, future rankings).

## Calibration checklist

- Confirm calibration is fit on training folds only.
- Verify calibrated probabilities sum to 1.
- Check calibration curve improves Brier score.

## Simulation checklist

- Confirm group stage format matches 2026 (12 groups, 32 qualifiers).
- Verify best third-place selection logic.
- Check probabilities sum to 1 at each stage.
- Ensure simulation uses calibrated model.

## Report checklist

- Each figure/table links to a script or notebook.
- Champion and challenger sections cite metrics and calibration.
- Business section includes tournament probabilities and commentary.
- Limitations and threats to validity are explicit.

## Reproducibility checklist

- Makefile targets run end-to-end without manual edits.
- Outputs stored in outputs/ with traceable names.
- Random seeds documented where used.
- Requirements and pyproject list all dependencies.
