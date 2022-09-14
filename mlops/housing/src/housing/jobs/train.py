from sklearn.ensemble import GradientBoostingRegressor

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

    reg = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.05,
                                       max_depth=3, max_features='sqrt',
                                       min_samples_leaf=15, min_samples_split=10,
                                       loss='huber', random_state =5)
    reg.fit(x,y)
    logging.info(f"Score of model: {reg.score(x, y)}")
    datalake.write_model(reg, config.date, "regression")
    logging.info("Training done.")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())
