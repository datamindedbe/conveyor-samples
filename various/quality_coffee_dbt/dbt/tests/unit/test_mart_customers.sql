{{ config(tags=["unit-test"]) }}

{% call dbt_unit_testing.test("customers", "Testing whether customer mart works as expected") %}

{% call dbt_unit_testing.mock_ref("stg_customers", {"input_format": "csv"}) %}
 customer_id::varchar, customer_name 
 '1', 'Francis De Groote'     
{% endcall %}

{% call dbt_unit_testing.mock_ref("orders", {"input_format": "csv"}) %}
order_id::varchar, customer_id::varchar, location_id::varchar, order_total, ordered_at::timestamp, tax_paid, count_food_items, count_drink_items, count_items, subtotal_drink_items, subtotal_food_items, subtotal, order_cost, location_name, is_food_order, is_drink_order
'404', '1', '3000', 106, '2020-01-01 12:34:56', 6, 1, 1, 2, 6, 94, 100, 0, 'Brussels', true, true
'404', '1', '3000', 106, '2020-01-02 12:34:59', 6, 1, 1, 2, 6, 94, 100, 0, 'Brussels', true, true
{% endcall %}

{% call dbt_unit_testing.expect({"input_format": "csv"}) %}
 customer_id::varchar, customer_name, count_lifetime_orders, first_ordered_at::timestamp, last_ordered_at::timestamp, lifetime_spend_pretax::float, lifetime_spend::float, customer_type
 1, 'Francis De Groote', 2, '2020-01-01 12:34:56', '2020-01-02 12:34:59', 200, 212, 'returning'
{% endcall %}

{% endcall %}
