import argparse

from openaq.common.spark import ClosableSparkSession, SparkLogger
from openaq.jobs import entrypoint

# this import is required to discover the jobs
# noinspection PyUnresolvedReferences
from openaq.jobs import sample

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="openaq-pyspark")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )
    parser.add_argument(
        "-j",
        "--jobs",
        nargs="+",
        dest="jobs",
        help="jobs that need to be executed",
        required=True,
    )
    args = parser.parse_args()

    with ClosableSparkSession("openaq-pyspark") as session:
        logger = SparkLogger(session)
        for job_name in args.jobs:
            logger.info(f"Executing job {job_name}")
            job = entrypoint.all[job_name]
            job(session, args.env, args.date)
