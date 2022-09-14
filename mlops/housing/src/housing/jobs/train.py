from sklearn.ensemble import GradientBoostingClassifier

import sys
import logging
import housing.datalake as datalake
from housing.config import Config, parse_args


def run(config: Config):
    logging.info("Training the classifier")
    df = datalake.load_parquet("features/training", config.date, "data")
    target = 'SalePrice'
    features = [ col for col in df.columns if col != target ]
    x, y = df[features], df[target]

    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=2).fit(x, y)
    score = clf.score(x, y)
    logging.info(f"Score of model: {score}")
    datalake.write_model(clf, config.date, "classifier")
    logging.info("Training done.")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())
