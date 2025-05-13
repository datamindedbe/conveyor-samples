import os
from collections.abc import Collection, Callable, Iterator
from argparse import ArgumentParser

import pyarrow as pa
import sqlalchemy as sa
import dlt
from connectorx import read_sql
from dlt.sources.credentials import ConnectionStringCredentials
from dlt.sources import DltSource, DltResource
from dlt.sources.sql_database import sql_database
from typing import Any, Optional

from dlt_example.validation.oracle import is_valid_db_object_name


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
        pipeline_name=pipeline_name,
        destination=destination,
        dataset_name=dataset_name,
    )
    source = data_source.with_resources(*table_names)

    info = pipeline.run(
        source,
        write_disposition="replace",
    )

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
    if (
        "BLOB" in type_name or "LOB" in type_name or "BFILE" in type_name
    ):  # lob is bfile
        return sa.LargeBinary()
    if "UROWID" in type_name:
        return sa.String(4000)  # max UROWID length in Oracle

    return None  # Let dlt handle other types


def convert_name_of_relation(s: str) -> str:
    """Return the name of the relation desired in the target system.

    E.g. you could have a view in a source system called 'orders_vw'
    and would wish it in the target system to have the name 'orders'.
    It's in functions like these that you can apply this logic.
    """

    return s


def relation_generator(
    conn_str: ConnectionStringCredentials = dlt.secrets.value,
    query: str = dlt.config.value,
    partition_on: str | None = None,
) -> Iterator[pa.Table]:
    allowed_core_count = min(
        len(os.sched_getaffinity(0)), 1
    )  # will differ from multiprocessing.cpu_count in constrained environments, like Docker containers.
    yield read_sql(
        conn=conn_str.to_native_representation(),
        query=query,
        partition_on=partition_on,
        partition_num=allowed_core_count,
        return_type="arrow",
        protocol="binary",
    )


def generic_incremental(
    schema_name: str,
    relation_name: str,
    connection_string: str,
    incremental_column: str,
    is_valid_db_object_name: Callable[[str], bool] = is_valid_db_object_name,
    relation_name_converter: Callable[[str], str] = convert_name_of_relation,
    relation_generator: Iterator[pa.Table] = relation_generator,
    partition_on: str | None = None,
) -> DltResource:
    """Return a dlt Resource suitable for incremental loading using ConnectorX's fast loading mechanism"""
    # Table names cannot always be bound using the db's main driver API (e.g. python-oracle can't*), so the developer is tasked with validating the table names.
    # *: See https://python-oracledb.readthedocs.io/en/latest/user_guide/bind.html#binding-column-and-table-names
    if not is_valid_db_object_name(relation_name):
        raise ValueError(
            f"'{relation_name}' is not a valid name for a relation (i.e. table, view)."
        )
    if not is_valid_db_object_name(schema_name):
        raise ValueError(f"'{schema_name}' is not a valid schema name.")
    query = f"SELECT * FROM {schema_name}.{relation_name}"
    resource = dlt.resource(
        name=relation_name_converter(relation_name),
        write_disposition="merge",
        standalone=True,
    )(relation_generator)(connection_string, query, partition_on)

    resource.apply_hints(incremental=dlt.sources.incremental(incremental_column))
    return resource


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "type",
        default="all",
        choices=("all", "inc", "full", "connx"),
        help="type of loading: incremental, full load or both",
    )
    args = parser.parse_args()

    if args.type in ("connx", "all"):
        incremental_load = dlt.config["incremental_with_connectorx"]
        pipe = dlt.pipeline(
            pipeline_name="foo", destination="duckdb", dataset_name="in_the_output"
        )
        source = generic_incremental(
            schema_name=incremental_load["schema"],
            relation_name=incremental_load["table_name"],
            connection_string="",
            partition_on=incremental_load["partition_column"],
            incremental_column=incremental_load["incremental_column"],
        )
        pipe.run(source, write_disposition="merge")

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
        full_data_source: DltSource = sql_database(
            schema=full_load["schema"], type_adapter_callback=type_adapter
        )
        full_load_select_tables_from_database(
            data_source=full_data_source,
            pipeline_name=full_load["pipeline_name"],
            destination=full_load["destination"],
            dataset_name=full_load["dataset_name"],
            table_names=full_load["table_name"],
        )
