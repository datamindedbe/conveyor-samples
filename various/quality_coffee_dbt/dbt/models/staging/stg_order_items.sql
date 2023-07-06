with

    source as (select * from {{ dbt_unit_testing.source("coffee", "raw_items") }}),

    renamed as (

        select

            -- --------  ids
            id as order_item_id,
            order_id,

            -- -------- properties
            sku as product_id

        from source

    )

select *
from renamed
