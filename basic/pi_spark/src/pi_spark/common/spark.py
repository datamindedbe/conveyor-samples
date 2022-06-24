import logging

from py4j.java_gateway import java_import
from pyspark.sql import SparkSession


def transform(self, f):
    return f(self)


class SparkLogger:
    def __init__(self, spark: SparkSession):
        conf = spark.sparkContext.getConf()
        app_id = conf.get("spark.app.id")
        app_name = conf.get("spark.app.name")

        log4j = spark._jvm.org.apache.log4j
        message_prefix = "<" + app_name + " " + app_id + ">"
        self.logger = log4j.LogManager.getLogger(message_prefix)

    def error(self, message):
        """Log an error.
        :param: Error message to write to log
        :return: None
        """
        self.logger.error(message)
        return None

    def warn(self, message):
        """Log an warning.
        :param: Error message to write to log
        :return: None
        """
        self.logger.warn(message)
        return None

    def info(self, message):
        """Log information.
        :param: Information message to write to log
        :return: None
        """
        self.logger.info(message)
        return None


class ClosableSparkSession:
    def __init__(
        self,
        app_name: str,
        master: str = None,
        spark_config: dict = {},
    ):
        self._app_name = app_name
        self._master = master
        self._spark_config = spark_config
        self._spark_session = None

    def __enter__(self):
        spark_builder = SparkSession.builder.appName(self._app_name).enableHiveSupport()

        # set master if needed
        if self._master:
            spark_builder = spark_builder.master(self._master)

        # set some default configuration
        spark_builder.config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        spark_builder.config("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

        # These values are set because of an issue with the current spark hive, glue connection
        # For more info see the conveyor docs:
        # https://docs.conveyordata.com/how-to-guides/troubleshooting/spark-pyspark-issues/#glue-orgapachehadoophivemetastoreapiinvalidobjectexception
        spark_builder.config("spark.sql.hive.metastorePartitionPruning", "false")
        spark_builder.config("spark.sql.hive.convertMetastoreParquet", "false")

        
        # add other config params
        for key, val in self._spark_config.items():
            spark_builder.config(key, val)

        # create the actual session
        self._spark_session = spark_builder.getOrCreate()

        return self._spark_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            logging.error(exc_tb)
        if self._spark_session:
            self._spark_session.stop()
