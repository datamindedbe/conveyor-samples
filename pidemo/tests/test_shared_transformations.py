from datetime import datetime

from pidemo.transformations.shared import add_ds
from tests.common.spark import get_test_spark_session, assert_frame_equal_with_sort

spark = get_test_spark_session()


def test_add_ds():
    date_string = "2020-01-01"
    date = datetime.strptime(date_string, "%Y-%m-%d").date()
    source_df = spark.createDataFrame(
        [("issue1", "high"), ("issue2", "low")], ["issue", "prio"]
    )
    expected = spark.createDataFrame(
        [("issue1", "high", date), ("issue2", "low", date)], ["issue", "prio", "ds"]
    )
    result = add_ds(date_string)(source_df)
    assert_frame_equal_with_sort(result, expected)
