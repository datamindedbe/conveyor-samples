import sys
import logging
import pandera as pa

import titanic.datalake as datalake
from titanic.config import Config, parse_args


schema = pa.DataFrameSchema({
        "PassengerId": pa.Column(int),
        "Survived": pa.Column(int, checks=pa.Check.isin([0,1])),
        "Pclass": pa.Column(int, checks=pa.Check.isin([0,1,2,3])),
        "Name": pa.Column(str),
        "Sex": pa.Column(str, checks=pa.Check(lambda s: s.isin(["male", "female"]))),
        "Age": pa.Column(float, checks=pa.Check.less_than(100, ignore_na=True), nullable=True),
        "SibSp": pa.Column(int),
        "Parch": pa.Column(int),
        "Ticket": pa.Column(str),
        "Fare": pa.Column(float),
        "Cabin": pa.Column(str, nullable=True),
        "Embarked": pa.Column(str, nullable=True),
    }, strict=False)


def run(config: Config):
    logging.info(f"Validating {config.asset} dataset for date {config.date}...")
    df = datalake.load_csv(f"{config.asset}.csv", bucket="datafy-cp-artifacts")
    df = schema(df)
    datalake.write_parquet(df, "valid", config.date, "data")
    logging.info(f"Done validating.")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())