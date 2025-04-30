MODEL (
  name sqlmesh_example.lineitem_summary_incremental,
  kind INCREMENTAL_BY_TIME_RANGE (
    -- How does this model kind behave?
    --   DELETE by time range, then INSERT
    time_column l_shipdate,

    -- How do I handle late-arriving data?
    --   Handle late-arriving events for the past 2 (2*1) days based on cron
    --   interval. Each time it runs, it will process today, yesterday, and
    --   the day before yesterday.
    lookback 2,
  ),

  -- Don't backfill data before this date
  start '2024-10-25',
  --   Daily at Midnight UTC (Even if not specified, the model will be run daily)
  cron '@daily',


  audits (
    UNIQUE_VALUES(columns = (unique_id)),
    NOT_NULL(columns = (unique_id))
  )
);

SELECT
    l_returnflag,
    l_linestatus,
    l_shipdate,
    MD5(l_returnflag || l_linestatus) AS unique_id,
    SUM(l_quantity)  AS sum_qty,
    SUM(l_extendedprice) AS sum_base_price,
    SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price,
    SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,
    AVG(l_quantity) AS avg_qty,
    AVG(l_extendedprice) AS avg_price,
    AVG(l_discount) AS avg_disc,
    COUNT(*) AS count_order
FROM SNOWFLAKE_SAMPLE_DATA.tpch_sf1.lineitem  
WHERE l_shipdate BETWEEN @start_dt AND @end_dt
GROUP BY
  l_returnflag,
  l_linestatus,
  l_shipdate
ORDER BY
  l_returnflag,
  l_linestatus,
  l_shipdate;
