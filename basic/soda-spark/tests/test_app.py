from datetime import datetime

from soda_spark_example.app import run
from tests.common.spark import get_test_spark_session

spark = get_test_spark_session()


def test_run():
    run(spark, "../soda.yaml")
