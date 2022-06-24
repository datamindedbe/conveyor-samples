import logging
from functools import lru_cache

from pandas.util.testing import assert_frame_equal
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


@lru_cache(maxsize=None)
def get_test_spark_session():
    return SparkSession.builder.master("local").getOrCreate()


def assert_frame_equal_with_sort(
    results: DataFrame, expected: DataFrame, check_nullability=None, **kwds
):
    try:
        if check_nullability:
            assert set(results.schema.fields) == set(expected.schema.fields)
        else:
            assert set(results.dtypes) == set(expected.dtypes)
    except AssertionError:
        logging.warning(results.schema)
        logging.warning(expected.schema)
        raise

    results_pandas = results.toPandas().sort_index(axis=1)
    results_pandas = results_pandas.sort_values(
        results_pandas.columns.values.tolist()
    ).reset_index(drop=True)
    expected_pandas = expected.toPandas().sort_index(axis=1)
    expected_pandas = expected_pandas.sort_values(
        expected_pandas.columns.values.tolist()
    ).reset_index(drop=True)
    return assert_frame_equal(results_pandas, expected_pandas, check_names=True, **kwds)
