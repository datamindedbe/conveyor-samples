import logging
from functools import lru_cache

from pandas.util.testing import assert_frame_equal
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


@lru_cache(maxsize=None)
def get_test_spark_session():
    return SparkSession.builder.master("local").getOrCreate()

