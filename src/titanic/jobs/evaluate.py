import titanic.datalake as datalake
from titanic.config import Config, parse_args

import sys
import logging


def run(config: Config):
    logging.info("Predicting titanic survival for test dataset.")
    
    df = datalake.load_parquet("features/testing", config.date, "data")
    target = 'Survived'
    features = [ col for col in df.columns if col != target ]
    x, y = df[features], df[target]

    classifier = datalake.load_model(config.date, "classifier")

    pred = classifier.predict(x)
    predictions_df = df.copy()
    predictions_df['Prediction'] = pred

    datalake.write_parquet(predictions_df, "evaluation", config.date, "data")
    accuracy = 100. * (pred == y).mean()
    logging.info(f"Prediction done with accuracy {accuracy}%.")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())
