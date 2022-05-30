import argparse
import logging
import sys

import requests
from typing import Optional


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description="samples_slack")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )
    args = parser.parse_args()
    logging.info(f"Using args: {args}")

    run(args.env, args.date)


def run(env: str, date: str):
    """Main ETL script definition.

    :return: None
    """
    # execute ETL pipeline
    raise Exception('Deliberate failing')


if __name__ == "__main__":
    main()
