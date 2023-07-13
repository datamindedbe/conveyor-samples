from datetime import datetime

from soda_spark_example.app import run
from tests.common.spark import get_test_spark_session, assert_frame_equal_with_sort

spark = get_test_spark_session()


def test_run():
    run(spark)
