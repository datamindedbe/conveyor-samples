import re
import sys
import logging
import pandas as pd
import numpy as np

import housing.datalake as datalake
from housing.config import Config, parse_args
from sklearn.model_selection import train_test_split


def run(config: Config):
    logging.info(f"Preparing features for dataset {config.asset} for date {config.date}...")
    df = datalake.load_parquet("valid", config.date, "data")

    features_df = df.copy()
    fill_missing_string_values_none(features_df)
    fill_missing_float_values_zero(features_df)
    fill_missing_int_values_zero(features_df)
    fill_columns_most_common_value(features_df)
    fill_functional_column(features_df)
    add_total_area(features_df)
    features_df = features_df.drop(
        ['Utilities'], axis=1
    )
    if config.asset == "train":
        training_features, test_features = train_test_split(features_df, test_size=0.2)
        datalake.write_parquet(training_features, "features/training", config.date, "data")
        datalake.write_parquet(test_features, "features/testing", config.date, "data")
    else:
        features_df = features_df.drop(['SalePrice'], axis=1)
        datalake.write_parquet(features_df, "features/predictions", config.date, "data")
    logging.info(f"Done extracting features.")


def fill_missing_string_values_none(df: pd.DataFrame):
    for col in ('GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'MasVnrType', 'MSSubClass'):
        df[col] = df[col].fillna('None')


def fill_missing_float_values_zero(df: pd.DataFrame):
    for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'MasVnrArea'):
        df[col] = df[col].fillna(0)


def fill_missing_int_values_zero(df: pd.DataFrame):
    for col in ('GarageYrBlt', 'GarageArea', 'GarageCars'):
        df[col] = df[col].fillna(0)


def fill_columns_most_common_value(df: pd.DataFrame):
    df['MSZoning'] = df['MSZoning'].fillna(df['MSZoning'].mode()[0])
    df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode()[0])
    df['KitchenQual'] = df['KitchenQual'].fillna(df['KitchenQual'].mode()[0])
    df['Exterior1st'] = df['Exterior1st'].fillna(df['Exterior1st'].mode()[0])
    df['Exterior2nd'] = df['Exterior2nd'].fillna(df['Exterior2nd'].mode()[0])
    df['SaleType'] = df['SaleType'].fillna(df['SaleType'].mode()[0])


def fill_functional_column(df: pd.DataFrame):
    df['Functional'] = df['Functional'].fillna('Typ')


def add_total_area(df: pd.DataFrame):
    df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())