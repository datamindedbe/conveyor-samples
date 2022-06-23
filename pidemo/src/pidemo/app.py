import argparse

import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.dataframe import DataFrame

from pidemo.common.spark import ClosableSparkSession, transform, SparkLogger
from pidemo.transformations.shared import add_ds


DataFrame.transform = transform


def main():
    parser = argparse.ArgumentParser(description="pidemo")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )    
    parser.add_argument(
        "-p", "--partitions", dest="partitions", help="number of partitions to calculate pi", required=False
    )
    args = parser.parse_args()

    with ClosableSparkSession("pidemo") as session:        
        run(session, args.env, args.date, int(args.partitions))


def run(spark: SparkSession, environment: str, date: str, partitions: int=2):
    """Main ETL script definition.

    :return: None
    """
    # execute ETL pipeline
    logger = SparkLogger(spark)
    logger.info(f"Executing job for {environment} on {date}")
    n = 100000 * partitions
    logger.info(f"Partitions: {partitions}")
    logger.info(f"n: {n}")
    def f(_: int) -> float:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    logger.info("Pi is roughly %f" % (4.0 * count / n))



if __name__ == "__main__":
    main()