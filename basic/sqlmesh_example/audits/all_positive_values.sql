-- Dummy custom audit to check if all values in a column are positive
AUDIT (
  name all_positive_values,
);
SELECT *
-- @this_model: Custom macro from sqlmesh, keeps information about the model name and kind of model, if it's incremental it will only run the audits on the current window
FROM @this_model 
WHERE
  @columns <= 0; 
