from collections.abc import Collection
from argparse import ArgumentParser

import sqlalchemy as sa
import dlt
from dlt.sources import DltSource
from dlt.sources.sql_database import sql_database
from typing import Any, Optional

# Incremental load: https://dlthub.com/docs/general-usage/incremental-loading
def incremental_load_select_tables_from_database(
    data_source: DltSource,
    pipeline_name: str,
    destination: str,
    dataset_name: str,
    table_name: Collection[str],
    incremental_column: str,
) -> None:
    """
    Loads selected tables from the database incrementally based on the specified column (usually, a timestamp).

    Args:
        data_source
        pipeline_name
        destination
        dataset_name: The dataset name used for loading data.
        table_name: A list of table names to be loaded.
        incremental_column: The column used to filter the new data for incremental loading, usually a timestamp.

    """
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name, destination=destination, dataset_name=dataset_name
    )

    source = data_source.with_resources(*table_name)

    for table in table_name:
        source.resources[table].apply_hints(
            incremental=dlt.sources.incremental(incremental_column)
        )

    info = pipeline.run(source, write_disposition="merge")

    print(info)


def full_load_select_tables_from_database(
    data_source: DltSource,
    pipeline_name: str,
    destination: str,
    dataset_name: str,
    table_names: Collection[str],
) -> None:
    """
    Performs a full load of selected tables from the database, replacing any existing data in the destination.

    Args:
        data_source
        pipeline_name
        destination
        dataset_name: The dataset name used for loading data.
        table_names: A list of table names to be loaded.

    """
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name, destination=destination, dataset_name=dataset_name
    )
    source = data_source.with_resources(*table_names)

    info = pipeline.run(source, write_disposition="replace")

    print(info)


def full_load_entire_database(
    data_source: DltSource, pipeline_name: str, destination: str, dataset_name: str
) -> None:
    """
    Performs a full load of the entire database, replacing any existing data in the destination.

    Args:
        data_source
        pipeline_name
        destination
        dataset_name: The dataset name used for loading data.

    """
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name, destination=destination, dataset_name=dataset_name
    )

    # Run the pipeline
    info = pipeline.run(data_source, write_disposition="replace")

    print(info)


def incremental_load_entire_database(
    data_source: DltSource,
    pipeline_name: str,
    destination: str,
    dataset_name: str,
    incremental_column: str,
) -> None:
    """
    Performs a full load of the entire database, replacing any existing data in the destination.

    Args:
        data_source
        pipeline_name
        destination
        dataset_name: The dataset name used for loading data.
        incremental_column: The column used to filter the new data for incremental loading, usually a timestamp.

    """
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name, destination=destination, dataset_name=dataset_name
    )

    for table in data_source.resources:
        data_source.resources[table].apply_hints(
            incremental=dlt.sources.incremental(incremental_column)
        )

    info = pipeline.run(data_source, write_disposition="merge")
    print(info)


def type_adapter(column_type: Any) -> Optional[Any]:
    """
    Adapt Oracle column types to SQLAlchemy types.

    Args:
        column_type: The Oracle column type

    Returns:
        Optional[Any]: The adapted SQLAlchemy type or None
    """
    type_name = str(column_type).upper()
    if "INTERVAL YEAR TO MONTH" in type_name:
        return sa.VARCHAR(255) 
    if "CLOB" in type_name or "NCLOB" in type_name:
        return sa.Text()
    if "BLOB" in type_name or "LOB" in type_name or "BFILE" in type_name: #lob is bfile
        return sa.LargeBinary()
    if "UROWID" in type_name:
        return sa.String(4000) # max UROWID length in Oracle

    return None # Let dlt handle other types


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "type",
        default="all",
        choices=("all", "inc", "full"),
        help="type of loading: incremental, full load or both",
    )
    args = parser.parse_args()

    if args.type in ("inc", "all"):
        incremental_load = dlt.config["incremental_load"]
        incremental_data_source: DltSource = sql_database(
            schema=incremental_load["schema"]
        )  # type: ignore
        incremental_load_select_tables_from_database(
            data_source=incremental_data_source,
            pipeline_name=incremental_load["pipeline_name"],
            destination=incremental_load["destination"],
            dataset_name=incremental_load["dataset_name"],
            table_name=incremental_load["table_name"],
            incremental_column=incremental_load["incremental_column"],
        )

    if args.type in ("full", "all"):
        full_load = dlt.config["full_load"]
        full_data_source: DltSource = sql_database(schema=full_load["schema"], type_adapter_callback=type_adapter) 
        full_load_select_tables_from_database(
            data_source=full_data_source,
            pipeline_name=full_load["pipeline_name"],
            destination=full_load["destination"],
            dataset_name=full_load["dataset_name"],
            table_names=full_load["table_name"],
        )
