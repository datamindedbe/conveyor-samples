
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

SELECT
    ds,
    city,
    parameter,
    avg(value) AS avg_value,
    min(value) AS min_value,
    max(value) AS max_value
FROM openaq_pyspark
GROUP BY ds, city, parameter

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
