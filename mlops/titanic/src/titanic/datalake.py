import logging
import tempfile
import joblib
import boto3
import awswrangler as wr
import pandas as pd


def get_bucket() -> str:
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='/conveyor-samples/bucket/name')
    logging.info(f"Using bucket {parameter['Parameter']['Value']}")
    return parameter['Parameter']['Value']


def key_prefix() ->str:
    return "titanic"


def load_csv(path: str) -> pd.DataFrame:
    s3path = f's3://{get_bucket()}/{key_prefix()}/raw/{path}'
    logging.info(f"Loading csv data from {s3path}")
    return wr.s3.read_csv(path=s3path)


def write_parquet(df: pd.DataFrame, path: str, date: str, name: str):
    s3path = f's3://{get_bucket()}/{key_prefix()}/{path}/date={date}/{name}.parquet'
    logging.info(f"Writing parquet data to {s3path}")
    wr.s3.to_parquet(df, path=s3path)


def load_parquet(path: str, date: str, name: str):
    s3path = f's3://{get_bucket()}/{key_prefix()}/{path}/date={date}/{name}.parquet'
    logging.info(f"Loading parquet data from {s3path}")
    return wr.s3.read_parquet(path=s3path)


def write_model(model, date: str, name: str):
    with tempfile.TemporaryFile() as temp_file:
        joblib.dump(model, temp_file)
        temp_file.seek(0)
        key = f'{key_prefix()}/model/date={date}/{name}.model'
        s3_resource = boto3.resource('s3')
        s3_resource.meta.client.put_object(Body=temp_file.read(), Bucket=get_bucket(), Key=key)


def load_model( date: str, name: str):
    with tempfile.TemporaryFile() as temp_file:
        key = f'{key_prefix()}/model/date={date}/{name}.model'
        s3_resource = boto3.resource('s3')
        s3_resource.meta.client.download_fileobj(Fileobj=temp_file, Bucket=get_bucket(), Key=key)
        temp_file.seek(0)
        return joblib.load(temp_file)