import dlt
from dlt.sources.sql_database import sql_database
from dlt.sources import DltSource


# Incremental load: https://dlthub.com/docs/general-usage/incremental-loading
def incremental_load_select_tables_from_database(
    data_source: DltSource,
    pipeline_name: str,
    destination: str,
    dataset_name: str,
    table_name: list[str],
    incremental_column: str,
) -> None:
    """
    Loads selected tables from the database incrementally based on the specified column (usually, a timestamp).

    Args:
        data_source (DltSource)
        pipeline_name (str)
        destination (str)
        dataset_name (str): The dataset name used for loading data.
        table_name (list[str]): A list of table names to be loaded.
        incremental_column (str): The column used to filter the new data for incremental loading, usually a timestamp.

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
    table_name: list[str],
) -> None:
    """
    Performs a full load of selected tables from the database, replacing any existing data in the destination.

    Args:
        data_source (DltSource)
        pipeline_name (str)
        destination (str)
        dataset_name (str): The dataset name used for loading data.
        table_name (list[str]): A list of table names to be loaded.

    """
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name, destination=destination, dataset_name=dataset_name
    )

    # Load the full table
    source = data_source.with_resources(*table_name)

    # Run the pipeline
    info = pipeline.run(source, write_disposition="replace")

    # Print the info
    print(info)


def full_load_entire_database(
    data_source: DltSource, pipeline_name: str, destination: str, dataset_name: str
) -> None:
    """
    Performs a full load of the entire database, replacing any existing data in the destination.

    Args:
        data_source (DltSource)
        pipeline_name (str)
        destination (str)
        dataset_name (str): The dataset name used for loading data.

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
        data_source (DltSource)
        pipeline_name (str)
        destination (str)
        dataset_name (str): The dataset name used for loading data.
        incremental_column (str): The column used to filter the new data for incremental loading, usually a timestamp.

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


def main():
    print("Hello from oracle-to-s3tables-dlthub!")


if __name__ == "__main__":
    main()

    incremental_data_source = sql_database(schema=dlt.config["incremental_load.schema"])
    incremental_load_select_tables_from_database(
        incremental_data_source,
        dlt.config["incremental_load.pipeline_name"],
        dlt.config["incremental_load.destination"],
        dlt.config["incremental_load.dataset_name"],
        dlt.config["incremental_load.table_name"],
        dlt.config["incremental_load.incremental_column"],
    )

    full_data_source = sql_database(schema=dlt.config["full_load.schema"])
    full_load_select_tables_from_database(
        full_data_source,
        dlt.config["full_load.pipeline_name"],
        dlt.config["full_load.destination"],
        dlt.config["full_load.dataset_name"],
        dlt.config["full_load.table_name"],
    )
