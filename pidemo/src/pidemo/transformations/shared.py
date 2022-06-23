from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import lit
from datetime import datetime


def add_ds(date: str):
    actual_date = datetime.strptime(date, "%Y-%m-%d").date()

    def inner(df: DataFrame):
        return df.withColumn("ds", lit(actual_date))

    return inner
