import tempfile
from datetime import datetime

from openaq.jobs.sample import load_data
from tests.common.spark import get_test_spark_session, assert_frame_equal_with_sort

spark = get_test_spark_session()


def test_partitioned_write():
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    date1_string = "2020-01-01"
    date2_string = "2020-01-02"
    date1 = datetime.strptime(date1_string, "%Y-%m-%d").date()
    date2 = datetime.strptime(date2_string, "%Y-%m-%d").date()
    date1_df = spark.createDataFrame(
        [("issue1", "high", date1), ("issue2", "low", date1)], ["issue", "prio", "ds"]
    )
    date2_df = spark.createDataFrame(
        [("issue3", "high", date2), ("issue4", "low", date2)], ["issue", "prio", "ds"]
    )
    expected = date1_df.union(date2_df)
    temppath = tempfile.TemporaryDirectory()
    load_data(spark, date1_df, database="default", path=temppath)
    load_data(spark, date2_df, database="default", path=temppath)
    result = spark.read.table("openaq_pyspark")
    assert_frame_equal_with_sort(result, expected)
