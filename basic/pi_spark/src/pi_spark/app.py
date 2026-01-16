import argparse

import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.dataframe import DataFrame

from pi_spark.common.spark import ClosableSparkSession, transform, SparkLogger

DataFrame.transform = transform


def main():
    parser = argparse.ArgumentParser(description="pi_spark")
    parser.add_argument(
        "-d",
        "--date",
        dest="date",
        help="date in format YYYY-mm-dd",
        required=True,
    )
    parser.add_argument(
        "-e",
        "--env",
        dest="env",
        help="environment we are executing in",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--partitions",
        dest="partitions",
        help="number of partitions to calculate pi",
        required=False,
    )
    parser.add_argument(
        "-i",
        "--iterations",
        dest="iterations",
        help="number of iterations per partition to calculate pi",
        required=False,
    )
    args = parser.parse_args()

    with ClosableSparkSession("pi_spark") as session:
        run(session, args.env, args.date, int(args.partitions), int(args.iterations))


def run(
    spark: SparkSession,
    environment: str,
    date: str,
    partitions: int = 1000,
    iterations: int = 10000000000,
):
    """Main ETL script definition.

    :return: None
    """
    # execute ETL pipeline
    logger = SparkLogger(spark)
    logger.info(f"Executing job for {environment} on {date}")
    logger.info(f"Partitions: {partitions}")
    logger.info(f"number of iterations/samples: {iterations}")

    def f(_: int) -> float:
        x, y = random(), random()
        return x * x + y * y < 1

    count = spark.sparkContext.parallelize(range(0, iterations), partitions).filter(f).count()
    logger.info("Pi is roughly %f" % (4.0 * count / iterations))


if __name__ == "__main__":
    main()
