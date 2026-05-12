"""Evaluate trained models on the test split."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import load

from src.evaluation.metrics import compute_classification_metrics
from src.models.challenger_poisson import PoissonModelBundle

logger = logging.getLogger(__name__)

DROP_COLUMNS = {
    "result",
    "date",
    "home_score",
    "away_score",
    "tournament",
    "match_id",
    "home_team",
    "away_team",
}


def split_by_date(
    df: pd.DataFrame,
    train_end: str,
    val_end: str,
    date_col: str = "date",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    train_df = df[df[date_col] < pd.to_datetime(train_end)]
    val_df = df[
        (df[date_col] >= pd.to_datetime(train_end))
        & (df[date_col] < pd.to_datetime(val_end))
    ]
    test_df = df[df[date_col] >= pd.to_datetime(val_end)]
    return train_df, val_df, test_df


def prepare_features(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    X = df.drop(columns=list(DROP_COLUMNS), errors="ignore")
    for col in feature_columns:
        if col not in X.columns:
            X[col] = pd.NA
    X = X[feature_columns]
    bool_cols = X.select_dtypes(include=["bool"]).columns
    for col in bool_cols:
        X[col] = X[col].astype(int)
    return X


def load_json(path: Path) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Evaluate models")
    parser.add_argument("--dataset", required=True, help="Match dataset CSV")
    parser.add_argument(
        "--models-dir", default="data/processed/models", help="Models dir"
    )
    parser.add_argument("--train-end", default="2022-01-01", help="Train end date")
    parser.add_argument("--val-end", default="2024-01-01", help="Validation end date")
    parser.add_argument(
        "--output",
        default="data/processed/metrics.csv",
        help="Output metrics CSV",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.dataset)
    _, _, test_df = split_by_date(df, args.train_end, args.val_end)

    models_dir = Path(args.models_dir)
    feature_columns = load_json(models_dir / "feature_columns.json")
    label_classes = load_json(models_dir / "label_classes.json")

    X_test = prepare_features(test_df, feature_columns)
    y_test = test_df["result"].astype(str).tolist()

    results = []
    model_paths = {
        "champion_xgboost": models_dir / "champion_xgboost.pkl",
        "challenger_logistic": models_dir / "challenger_logistic.pkl",
        "challenger_lightgbm": models_dir / "challenger_lightgbm.pkl",
        "challenger_poisson": models_dir / "challenger_poisson.pkl",
    }

    for name, path in model_paths.items():
        if not path.exists():
            logger.warning("Model not found: %s", path)
            continue

        model = load(path)
        if isinstance(model, PoissonModelBundle):
            proba_df = model.predict_proba(X_test)
            y_proba = proba_df[label_classes].to_numpy()
        else:
            y_proba = model.predict_proba(X_test)

        metrics = compute_classification_metrics(y_test, y_proba, label_classes)
        metrics["model"] = name
        results.append(metrics)

    results_df = pd.DataFrame(results).sort_values("log_loss")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    logger.info("Saved metrics to %s", output_path)


if __name__ == "__main__":
    main()
