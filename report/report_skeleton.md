# WC2026 Prediction Report - Skeleton

This skeleton matches the required academic structure and references the repo assets to use.

## 1. Define the problem

**Objective**: Formalize the task as multi-class classification (W/D/L) for group-stage matches and produce a Monte Carlo tournament simulation for qualification and title probabilities.

**Recommended subsections**

- Problem formulation and decision context
- Target definition (W/D/L) and prediction horizon
- Scope: group-stage predictions + knockout simulation
- Success criteria (log-loss + calibration) and deliverables
- Constraints and assumptions (data coverage, lineups, neutral venues)

**Figures / tables**

- Tournament format diagram (48 teams, 12 groups, R32)
- Pipeline overview (data -> features -> models -> simulation)

**Key messages**

- The project is probabilistic: we need calibrated probabilities, not point forecasts.
- Tournament outcome requires simulation, not single-match prediction.

**Repo assets to cite**

- notebooks/01_eda.ipynb
- notebooks/05_wc2026_simulation.ipynb
- src/simulation/group_stage.py
- src/simulation/knockout_stage.py

## 2. Describe and comment the dataset

**Objective**: Describe sources, coverage, quality controls, and the final match-level dataset.

**Recommended subsections**

- Data sources (international results, FIFA rankings, FBref club stats, WC schedule)
- Time coverage and filtering (official matches, 2010-2024)
- Key columns and joins (team names, dates, neutral flag)
- Missing values and data quality checks
- Target distribution (W/D/L)

**Figures / tables**

- Timeline of matches (count by year)
- Missingness heatmap or top missing features table
- Target distribution bar chart

**Key messages**

- The dataset integrates match results, rankings, and squad strength proxies.
- Filtering and alignment by date prevent leakage.

**Repo assets to cite**

- build_dataset.py
- src/data_collection/data_loader.py
- src/features/feature_builder.py
- data/processed/match_dataset.csv
- notebooks/01_eda.ipynb

## 3. Champion approach

**Objective**: Present the champion model, feature set, training protocol, and calibration strategy.

**Recommended subsections**

- Feature blocks: Elo, rolling form, FIFA ranks, squad aggregates, context
- Model choice: XGBoost for non-linear tabular interactions
- Calibration: isotonic (required for Monte Carlo)
- Training split: time-based (train < 2022, val 2022-2023, test 2024)
- Hyperparameters and rationale
- Interpretation via SHAP

**Figures / tables**

- Feature importance (model native)
- SHAP summary plot
- Calibration curve (reliability diagram)
- Log-loss table vs challengers

**Key messages**

- Calibration is the core requirement for simulation quality.
- Champion wins on log-loss and calibration, not accuracy alone.

**Repo assets to cite**

- src/models/champion_xgboost.py
- src/models/calibration.py
- train_models.py
- evaluate.py
- src/evaluation/shap_analysis.py
- notebooks/03_model_training.ipynb
- notebooks/04_evaluation.ipynb

## 4. Challengers

**Objective**: Present three alternative models and justify why the champion is superior.

**Recommended subsections**

- Challenger 1: Logistic regression (baseline, interpretability)
- Challenger 2: LightGBM (fast gradient boosting)
- Challenger 3: Double Poisson (goal-based modeling)
- Comparison summary (log-loss, brier, calibration)

**Figures / tables**

- Metrics comparison table (log-loss, accuracy, brier)
- Calibration curve overlay (champion vs challengers)

**Key messages**

- Baselines are competitive but less calibrated than the champion.
- Poisson model is academically strong for goals but less direct for W/D/L.

**Repo assets to cite**

- src/models/challenger_logistic.py
- src/models/challenger_lightgbm.py
- src/models/challenger_poisson.py
- evaluate.py
- notebooks/03_model_training.ipynb

## 5. Discuss the result from a data science standpoint

**Objective**: Interpret results, quantify uncertainty, and validate robustness.

**Recommended subsections**

- Model comparison on test period
- Calibration quality and reliability
- Feature sensitivity and stability
- Robustness checks (remove FIFA ranks, alternative splits)
- Error analysis (upsets, confederation effects)

**Figures / tables**

- Metrics table (test set)
- Calibration plots
- SHAP summary + example explanations

**Key messages**

- Champion model balances predictive power and probability quality.
- Some errors reflect inherent football randomness, not model flaws.

**Repo assets to cite**

- src/evaluation/metrics.py
- src/evaluation/temporal_cv.py
- src/evaluation/shap_analysis.py
- data/processed/metrics.csv
- notebooks/04_evaluation.ipynb

## 6. Discuss the result from a business (application) standpoint

**Objective**: Translate model outputs into tournament insights and decision metrics.

**Recommended subsections**

- Simulation design and assumptions
- Qualification and title probabilities
- Scenario analysis (best / median / worst outcomes)
- Comparison with bookmaker probabilities (edge analysis)

**Figures / tables**

- Win probability bar chart
- Stage reach probabilities heatmap
- Top 10 teams table
- Bookmaker comparison table

**Key messages**

- Monte Carlo outputs provide actionable tournament-level probabilities.
- Calibration ensures that simulated distributions are meaningful.

**Repo assets to cite**

- simulate_wc2026.py
- src/simulation/tournament_simulator.py
- src/simulation/bookmaker_benchmark.py
- data/processed/wc2026_simulation.csv
- notebooks/05_wc2026_simulation.ipynb

## 7. Conclude

**Objective**: Summarize findings, limitations, and next steps.

**Recommended subsections**

- Summary of performance and simulation insights
- Limitations (squad uncertainty, data coverage)
- Future work (dynamic squads, player injury modeling)

**Figures / tables**

- None (optional short recap table)

**Key messages**

- The project delivers a calibrated, reproducible workflow for WC2026.
- Future improvements center on lineup and availability uncertainty.
