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
    add_gender_feature(features_df)
    add_age_feature(features_df)
    add_family_size_feature(features_df)
    add_has_cabin_feature(features_df)
    add_categorical_fare_feature(features_df)
    add_title_feature(features_df)
    features_df = features_df.drop(
        ['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked', 'SibSp', 'Parch'], axis=1
    )
    if config.asset == "train":
        features_df = features_df.drop(['PassengerId'], axis=1)
        training_features, test_features = train_test_split(features_df, test_size=0.2)
        datalake.write_parquet(training_features, "features/training", config.date, "data")
        datalake.write_parquet(test_features, "features/testing", config.date, "data")
    else:
        features_df = features_df.drop(['Survived'], axis=1)
        datalake.write_parquet(features_df, "features/predictions", config.date, "data")
    logging.info(f"Done extracting features.")


def add_has_cabin_feature(df: pd.DataFrame):
    # if NA => 0 else 1
    def _is_nan(x):
        if isinstance(x, type(np.nan)):
            return 0
        return 1
    df['HasCabin'] = df['Cabin'].apply(_is_nan)


def add_categorical_fare_feature(df: pd.DataFrame):
    df['Fare'] = df['Fare']. \
        groupby([df['SexNumerical'], df['Pclass']]). \
        apply(lambda x: x.fillna(x.median()))
    df['CategoricalFare'] = pd.qcut(df['Fare'], 4, labels = [0, 1, 2, 3]).astype(int)

    
def add_gender_feature(df: pd.DataFrame):
    sexes = sorted(df['Sex'].unique())
    genders_mapping = dict(zip(sexes, range(0, len(sexes) + 1)))
    df['SexNumerical'] = df['Sex'].map(genders_mapping).astype(int)


def add_age_feature(df: pd.DataFrame):
    df['Age'] = df['Age']. \
        groupby([df['SexNumerical'], df['Pclass']]). \
        apply(lambda x: x.fillna(x.median()))


def add_family_size_feature(df: pd.DataFrame):
    df['FamilySize'] = df['SibSp'] + df['Parch']
    
    
def add_title_feature(df: pd.DataFrame):
    def find_title(x):
        title_search = re.search(' ([A-Za-z]+)\.', x)
        if title_search:
            title = title_search.group(1)
            if title in ['Mlle', 'Ms']:
                return 'Miss'

            elif title in ['Mme', 'Mrs']:
                return 'Mrs'
            elif title=='Mr':
                return 'Mr'           
            else:
                return 'Rare'
        return ""
    
    return_title= df['Name'].apply(find_title)
    dict_title = {'Miss': 1, 'Mrs':2, 'Mr':3, 'Rare':4}
    df['Title'] = return_title.replace(dict_title)
    

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())