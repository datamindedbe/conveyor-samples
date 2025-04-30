MODEL (
  name sqlmesh_example.lineitem_summary,
  kind FULL,
  cron '@daily',
  tags ['tpch', 'aggregation'],
  start '2024-10-25',
  audits (
    UNIQUE_VALUES(columns = (unique_id)),
    NOT_NULL(columns = (l_returnflag, l_linestatus)),
    all_positive_values(columns = (sum_base_price))
  )
);

SELECT
  l_returnflag,
  l_linestatus,
  MD5(l_returnflag || l_linestatus) AS unique_id,
  SUM(l_quantity) AS sum_qty,
  SUM(l_extendedprice) AS sum_base_price,
  SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price,
  SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,
  AVG(l_quantity) AS avg_qty,
  AVG(l_extendedprice) AS avg_price,
  AVG(l_discount) AS avg_disc,
  COUNT(*) AS count_order
FROM
  SNOWFLAKE_SAMPLE_DATA.tpch_sf1.lineitem
WHERE
  l_shipdate <= DATEADD(day, -90, TO_DATE('1998-12-01'))
GROUP BY
  l_returnflag,
  l_linestatus
ORDER BY
  l_returnflag,
  l_linestatus;