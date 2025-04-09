import dlt
from dlt.sources.sql_database import sql_database
from dlt.sources.credentials import ConnectionStringCredentials
from dlt.sources import DltSource
from chess import source

def load_incremental_table_resource(data_source: DltSource, pipeline_name:str, 
                                    destination:str, dataset_name:str, table_name:str, primary_key:str) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=destination,
        dataset_name=dataset_name
    )

    source = data_source.with_resources(*table_name)

    # only load rows whose incremental column value is greater than the last pipeline run
    # source.apply_hints(incremental=dlt.sources.incremental(incremental_column))

    info = pipeline.run(source, write_disposition="merge", primary_key=primary_key)

    print(info)



if __name__ == '__main__':
    pipeline_name = dlt.config["incremental_load.pipeline_name"]
    destination = dlt.config["incremental_load.destination"]
    dataset_name = dlt.config["incremental_load.dataset_name"]
    table_name = dlt.config["incremental_load.table_name"]
    primary_key = dlt.config["incremental_load.primary_key"]

    data_source = source(
    ["magnuscarlsen", "vincentkeymer", "dommarajugukesh", "rpragchess"],
    start_month="2022/11",
    end_month="2023/01",
    )
    
    load_incremental_table_resource(data_source, pipeline_name, destination, dataset_name, table_name, primary_key)
