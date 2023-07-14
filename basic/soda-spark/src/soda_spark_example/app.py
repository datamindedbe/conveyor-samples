import argparse

from pyspark.sql import SparkSession, types
from pyspark.sql import Row
from pyspark.sql.dataframe import DataFrame
from soda.scan import Scan

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
    parser.add_argument(
        "-s", "--sode-location", dest="soda_location", help="location of the soda.yaml", required=False, default="/opt/spark/work-dir/soda.yaml",
    )
    args = parser.parse_args()

    with ClosableSparkSession("soda-spark") as session:
        run(session, args.soda_location)


def data(spark):
    id = "a76824f0-50c0-11eb-8be8-88e9fe6293fd"
    df = spark.createDataFrame(
        [
            {"id": id, "name": "Paula Landry", "email": "p@gmail.com"},
            {"id": id, "name": "Kevin Crawford", "email": "l@gmail.com"},
            {"id": "12", "name": "John Smith", "email": "email"},
        ],
        schema=types.StructType(
            [
                types.StructField("id", types.StringType()),
                types.StructField("name", types.StringType()),
                types.StructField("email", types.StringType()),
            ]
        ),
    )
    df.createOrReplaceTempView("users")

def run(spark: SparkSession, soda_location: str):
    """Main ETL script definition.

    :return: None
    """

    logger = SparkLogger(spark)
    logger.info("Using soda data")
    data(spark)
    scan = Scan()
    scan.set_scan_definition_name("test")
    scan.set_data_source_name("spark_df")
    scan.add_spark_session(spark)
    scan.add_sodacl_yaml_file(file_path=soda_location)
    scan.execute()
    logger.info("Showing the measurements")
    logger.info(scan.get_logs_text())


if __name__ == "__main__":
    main()

