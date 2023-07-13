import argparse

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.dataframe import DataFrame
from sodaspark import scan

from soda_spark_example.common.spark import ClosableSparkSession, transform, SparkLogger


DataFrame.transform = transform


def main():
    parser = argparse.ArgumentParser(description="soda-spark")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )
    args = parser.parse_args()

    with ClosableSparkSession("soda-spark") as session:
        run(session, args.env, args.date)


def data(spark):
    id = "a76824f0-50c0-11eb-8be8-88e9fe6293fd"
    return spark.createDataFrame([
        {"id": id, "name": "Paula Landry", "size": 3006},
        {"id": id, "name": "Kevin Crawford", "size": 7243},
    ])


def scan_definition():
    return  ("""
table_name: demodata
metrics:
- row_count
- max
- min_length
tests:
- row_count > 0
columns:
  id:
    valid_format: uuid
    tests:
    - invalid_percentage == 0
sql_metrics:
- sql: |
    SELECT sum(size) as total_size_us
    FROM demodata
    WHERE country = 'US'
  tests:
  - total_size_us > 5000
""")

def run(spark: SparkSession, environment: str, date: str):
    """Main ETL script definition.

    :return: None
    """

    logger = SparkLogger(spark)
    logger.info("Using soda data")
    measurements, test_results, errors  = scan.execute(scan_definition(), data(spark), as_frames=True)
    measurements.show()
    test_results.show()


if __name__ == "__main__":
    main()
