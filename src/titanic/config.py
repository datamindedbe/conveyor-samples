import argparse

class Config:
    def __init__(self, asset: str, date: str):
        self.date = date
        self.asset = asset


def parse_args() -> Config:
    parser = argparse.ArgumentParser(description="mlbasic")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-a", "--asset", dest="asset", help="Asset you want to ingest or load", required=False
    )
    args = parser.parse_args()
    return Config(args.asset, args.date)