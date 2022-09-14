import re
import sys
import logging
import pandas as pd
import numpy as np
from scipy.stats import skew
from sklearn.preprocessing import LabelEncoder

import housing.datalake as datalake
from housing.config import Config, parse_args
from sklearn.model_selection import train_test_split
from scipy.special import boxcox1p


def run(config: Config):
    logging.info(f"Preparing features for dataset {config.asset} for date {config.date}...")
    df = datalake.load_parquet("valid", config.date, "data")

    features_df = df.copy()
    fill_missing_string_values_none(features_df)
    fill_missing_float_values_zero(features_df)
    fill_missing_int_values_zero(features_df)
    fill_columns_most_common_value(features_df)
    fill_missing_values_functional_column(features_df)
    fill_missing_lot_frontage(features_df)

    add_feature_total_area(features_df)
    features_df = features_df.drop(
        ['Utilities', 'MSZoning', 'LandContour','LotConfig','Neighborhood','Condition1','Condition2','BldgType',
        'HouseStyle','RoofStyle','RoofMatl','Exterior1st','Exterior2nd','MasVnrType','Foundation', 'Heating',
        'Electrical', 'GarageType', 'MiscFeature', 'SaleType', 'SaleCondition'], axis=1
    )

    features_df = log_transform_saleprice(features_df)
    label_encode_categorical_values(features_df)
    features_df = convert_categorical_values_to_dummies(features_df)
    correct_skewed_numerical_features(features_df)

    if config.asset == "train":
        training_features, test_features = train_test_split(features_df, test_size=0.2)
        training_features = remove_outliers(training_features)
        datalake.write_parquet(training_features, "features/training", config.date, "data")
        datalake.write_parquet(test_features, "features/testing", config.date, "data")
    else:
        features_df = features_df.drop(['SalePrice'], axis=1)
        datalake.write_parquet(features_df, "features/predictions", config.date, "data")
    logging.info(f"Done extracting features.")


def fill_missing_string_values_none(df: pd.DataFrame):
    for col in ('GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC', 'MiscFeature', 'Alley', 'Fence',
                'FireplaceQu', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'MasVnrType',
                'MSSubClass'):
        df[col] = df[col].fillna('None')


def fill_missing_float_values_zero(df: pd.DataFrame):
    for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'MasVnrArea'):
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


def fill_missing_values_functional_column(df: pd.DataFrame):
    df['Functional'] = df['Functional'].fillna('Typ')


def add_feature_total_area(df: pd.DataFrame):
    df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']


def convert_categorical_values_to_dummies(df: pd.DataFrame):
    return pd.get_dummies(df)


def remove_outliers(df: pd.DataFrame):
    return df.drop(df[(df['GrLivArea'] > 4000) & (df['SalePrice'] < 300000)].index)


def log_transform_saleprice(df: pd.DataFrame):
    # make target function normal distribution which makes it perfect for linear models
    return df.drop(df[(df['GrLivArea'] > 4000) & (df['SalePrice'] < 300000)].index)


def label_encode_categorical_values(df: pd.DataFrame):
    cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond',
            'ExterQual', 'ExterCond', 'HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1',
            'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope',
            'LotShape', 'PavedDrive', 'Street', 'Alley', 'CentralAir', 'MSSubClass', 'OverallCond',
            'YrSold', 'MoSold')
    for c in cols:
        lbl = LabelEncoder()
        lbl.fit(list(df[c].values))
        df[c] = lbl.transform(list(df[c].values))


def fill_missing_lot_frontage(df: pd.DataFrame):
    # Use the median of the neighbors to define the lot frontage.
    df["LotFrontage"] = df.groupby("Neighborhood")["LotFrontage"].transform(
        lambda x: x.fillna(x.median()))


def correct_skewed_numerical_features(df: pd.DataFrame):
    numeric_feats = df.dtypes[df.dtypes != "string"].index
    skewed_feats = df[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
    skewness = pd.DataFrame({'Skew': skewed_feats})
    skewness = skewness[abs(skewness) > 0.75]
    logging.info(f"Number of skewed features: {len(skewness)}")
    skewed_features = skewness.index
    lam = 0.15
    for feat in skewed_features:
        df[feat] = boxcox1p(df[feat], lam)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())
