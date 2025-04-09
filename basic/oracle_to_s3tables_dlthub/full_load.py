import dlt
from dlt.sources.sql_database import sql_database
from dlt.sources.credentials import ConnectionStringCredentials
from dlt.sources import DltSource
from chess import source

def load_full_table_resource(data_source: DltSource, pipeline_name:str, destination:str, 
                             dataset_name:str, table_name:list[str]) -> None:
    """Load a full table, replacing existing data."""
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=destination,
        dataset_name=dataset_name
    )

    # Load the full table
    source = data_source.with_resources(*table_name)

    # Run the pipeline
    info = pipeline.run(source, write_disposition="replace")

    # Print the info
    print(info)

if __name__ == '__main__':
    pipeline_name = dlt.config["full_load.pipeline_name"]
    destination = dlt.config["full_load.destination"]
    dataset_name = dlt.config["full_load.dataset_name"]
    table_name = dlt.config["full_load.table_name"]
    data_source = source(
        ["magnuscarlsen", "vincentkeymer", "dommarajugukesh", "rpragchess"],
        start_month="2022/11",
        end_month="2022/12",
    )
    load_full_table_resource(data_source, pipeline_name, destination, dataset_name, table_name)
