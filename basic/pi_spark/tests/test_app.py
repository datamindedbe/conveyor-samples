from datetime import datetime

from pi_spark.app import run
from tests.common.spark import get_test_spark_session, assert_frame_equal_with_sort

spark = get_test_spark_session()


def test_pi_demo_runs():
    date_string = "2020-01-01"    
    result = run(spark, "dev", date_string, 2)
    