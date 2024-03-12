{{ config(materialized='external') }}

with

source as (

    select * from {{ source('ecom', 'raw_products') }}

),

renamed as (

    select

        ----------  ids
        sku as product_id,

        ---------- properties
        name as product_name,
        type as product_type,
        description as product_description,
        (price / 100.0)::float as product_price,


        ---------- derived
        case
            when type = 'food' then 1
            else 0
        end is_food_item,

        case
            when type = 'beverage' then 1
            else 0
        end is_drink_item

    from source

)

select * from renamed
