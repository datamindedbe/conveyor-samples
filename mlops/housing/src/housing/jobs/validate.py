import sys
import logging
import pandera as pa

import housing.datalake as datalake
from housing.config import Config, parse_args


schema = pa.DataFrameSchema({
        "Id": pa.Column(int),
        "MSSubClass": pa.Column(int),
        "MSZoning": pa.Column(str),
        "LotFrontage": pa.Column(int),
        "LotArea": pa.Column(int),
        "Street": pa.Column(str),
        "Alley": pa.Column(str),
        "LotShape": pa.Column(str),
        "LandContour": pa.Column(str),
        "Utilities": pa.Column(str),
        "LotConfig": pa.Column(str),
        "LandSlope": pa.Column(str),
        "Neighborhood": pa.Column(str),
        "Condition1": pa.Column(str),
        "Condition2": pa.Column(str),
        "BldgType": pa.Column(str),
        "HouseStyle": pa.Column(str),
        "OverallQual": pa.Column(int),
        "OverallCond": pa.Column(int),
        "YearBuilt": pa.Column(int),
        "YearRemodAdd": pa.Column(int),
        "RoofStyle": pa.Column(str),
        "RoofMatl": pa.Column(str),
        "Exterior1st": pa.Column(str),
        "Exterior2nd": pa.Column(str),
        "MasVnrType": pa.Column(str),
        "MasVnrArea": pa.Column(int),
        "ExterQual": pa.Column(str),
        "ExterCond": pa.Column(str),
        "Foundation": pa.Column(str),
        "BsmtQual": pa.Column(str),
        "BsmtCond": pa.Column(str),
        "BsmtExposure": pa.Column(str),
        "BsmtFinType1": pa.Column(int),
        "BsmtFinSF1": pa.Column(str),
        "BsmtFinType2": pa.Column(int),
        "BsmtFinSF2": pa.Column(int),
        "BsmtUnfSF": pa.Column(int),
        "TotalBsmtSF": pa.Column(str),
        "Heating": pa.Column(str),
        "HeatingQC": pa.Column(str),
        "CentralAir": pa.Column(str),
        "Electrical": pa.Column(str),
        "1stFlrSF": pa.Column(str),
        "2ndFlrSF": pa.Column(int),
        "LowQualFinSF": pa.Column(int),
        "GrLivArea": pa.Column(int),
        "BsmtFullBath": pa.Column(int),
        "BsmtHalfBath": pa.Column(int),
        "FullBath": pa.Column(int),
        "HalfBath": pa.Column(int),
        "BedroomAbvGr": pa.Column(int),
        "KitchenAbvGr": pa.Column(int),
        "KitchenQual": pa.Column(str),
        "TotRmsAbvGrd": pa.Column(int),
        "Functional": pa.Column(str),
        "Fireplaces": pa.Column(int),
        "FireplaceQu": pa.Column(str),
        "GarageType": pa.Column(str),
        "GarageYrBlt": pa.Column(int),
        "GarageFinish": pa.Column(str),
        "GarageCars": pa.Column(int),
        "GarageArea": pa.Column(int),
        "GarageQual": pa.Column(str),
        "GarageCond": pa.Column(str),
        "PavedDrive": pa.Column(str),
        "WoodDeckSF": pa.Column(int),
        "OpenPorchSF": pa.Column(int),
        "EnclosedPorch": pa.Column(int),
        "3SsnPorch": pa.Column(int),
        "ScreenPorch": pa.Column(int),
        "PoolArea": pa.Column(int),
        "PoolQC": pa.Column(str),
        "Fence": pa.Column(str),
        "MiscFeature": pa.Column(str),
        "MiscVal": pa.Column(int),
        "MoSold": pa.Column(int),
        "YrSold": pa.Column(int),
        "SaleType": pa.Column(str),
        "SaleCondition": pa.Column(str),
        "SalePrice": pa.Column(int),
    }, strict=False)


def run(config: Config):
    logging.info(f"Validating {config.asset} dataset for date {config.date}...")
    df = datalake.load_csv(f"{config.asset}.csv")
    df = schema(df)
    datalake.write_parquet(df, "valid", config.date, "data")
    logging.info(f"Done validating.")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    run(parse_args())