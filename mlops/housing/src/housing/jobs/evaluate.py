import housing.datalake as datalake
from housing.config import Config, parse_args
from sklearn.model_selection import cross_val_score, KFold

import numpy as np
import pandas as pd
import sys
import logging


def run(config: Config):
    logging.info("Predicting housing sale price for test dataset.")
    
    df = datalake.load_parquet("features/testing", config.date, "data")
    target = 'SalePrice'
    features = [ col for col in df.columns if col != target ]
    x, y = df[features], df[target]

    reg = datalake.load_model(config.date, "regression")

    pred = reg.predict(x)
    predictions_df = df.copy()
    predictions_df['Prediction'] = pred

    datalake.write_parquet(predictions_df, "evaluation", config.date, "data")
    score = rmsle_cv(x, y, reg)
    logging.info(f"Gboost score: {score.mean():.4f} ({score.std():.4f})")


def rmsle_cv(features: pd.DataFrame, target: pd.DataFrame, model):
    n_folds = 5
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(features.values)
    return np.sqrt(-cross_val_score(model, features.values, target.values, scoring="neg_mean_squared_error", cv=kf))


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())
