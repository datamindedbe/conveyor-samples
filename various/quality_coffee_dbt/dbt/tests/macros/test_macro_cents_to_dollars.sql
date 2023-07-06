with
    input as (
        select 0 as id, 420 as input_col, 4.20 as expected_output_col  -- basic case
        union all
        select 1 as id, 0 as input_col, 0 as expected_output_col  -- zero
        union all
        select 2 as id, 100 as input_col, 1 as expected_output_col  -- exact integer
        union all
        select 3 as id, 987654321 as input_col, 9876543.21 as expected_output_col  -- larger numbers
    ),
    macro_output as (select id, {{ cents_to_dollars("input_col") }} as macro_output_col from input)
select input.id, input_col, expected_output_col, macro_output_col
from input
join macro_output on input.id = macro_output.id
where macro_output.macro_output_col != input.expected_output_col
