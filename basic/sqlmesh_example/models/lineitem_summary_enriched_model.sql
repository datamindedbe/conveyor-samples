-- Dummy enriched model based on lineitem_summary
MODEL (
  name sqlmesh_example.lineitem_summary_enriched,
  kind VIEW, 
  tags ['tpch', 'enrichment'],
);

WITH summary_data AS (
  SELECT * FROM sqlmesh_example.lineitem_summary 
)
SELECT
  sd.*, -- Select all original columns from the summary_data CTE
  -- Add a new derived feature: average charge per order
  -- Use NULLIF to prevent division by zero if count_order is 0
  sd.sum_charge / NULLIF(sd.count_order, 0) AS avg_charge_per_order
FROM summary_data AS sd;



