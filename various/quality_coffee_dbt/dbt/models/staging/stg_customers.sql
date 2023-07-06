{{ config(contract={"enabled": true}) }}
with

    source as (select * from {{ dbt_unit_testing.source("coffee", "raw_customers") }}),

    renamed as (

        select

            -- --------  ids
            id as customer_id,

            -- -------- properties
            name as customer_name

        from source

    )

select *
from renamed
