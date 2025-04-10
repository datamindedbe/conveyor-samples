import dlt
from dlt.sources.sql_database import sql_database
from dlt.sources import DltSource

# Incremental load: https://dlthub.com/docs/general-usage/incremental-loading
def load_incremental_table_resource(data_source: DltSource, pipeline_name:str, destination:str, 
                                    dataset_name:str, table_name:list[str], incremental_column:str) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=destination,
        dataset_name=dataset_name
    )

    source = data_source.with_resources(*table_name)
    # only load rows whose incremental column value is greater than the last pipeline run
    for table in table_name:
        source.resources[table].apply_hints(incremental=dlt.sources.incremental(incremental_column))

    info = pipeline.run(source, write_disposition="merge")

    print(info)



if __name__ == '__main__':
    pipeline_name = dlt.config["incremental_load.pipeline_name"]
    destination = dlt.config["incremental_load.destination"]
    dataset_name = dlt.config["incremental_load.dataset_name"]
    table_name = dlt.config["incremental_load.table_name"]
    incremental_column = dlt.config["incremental_load.incremental_column"]
    schema = dlt.config["incremental_load.schema"]
    data_source = sql_database(schema=schema)
    load_incremental_table_resource(data_source, pipeline_name, destination, dataset_name, table_name, incremental_column)
