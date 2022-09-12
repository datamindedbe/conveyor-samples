import sys
import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, 
                              GradientBoostingClassifier, ExtraTreesClassifier)

import housing.datalake as datalake
from housing.config import Config, parse_args


def run(config: Config):
    logging.info("Training the classifier")
    df = datalake.load_parquet("features/training", config.date, "data")
    target = 'Survived'
    features = [ col for col in df.columns if col != target ]
    x, y = df[features], df[target]

    parameters = {
        "random_state": 2,
    }
    rf = RandomForestClassifier(**parameters)
    et = ExtraTreesClassifier(**parameters)
    ada = AdaBoostClassifier(**parameters)
    gb = GradientBoostingClassifier(**parameters)
    models = [rf, et, ada, gb]
    model_names = ['RandomForest', 'ExtraTrees', 'Ada', 'GradientBoost']

    clf = VotingClassifier(voting='soft', estimators=[(name, m) for name, m in zip(model_names, models)])
    clf = clf.fit(x, y.astype('int'))

    datalake.write_model(clf, config.date, "classifier")
    logging.info("Training done.")
    


def get_target_from_df(df: pd.DataFrame) -> np.array:
    return df['Survived'].astype('int').values


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())