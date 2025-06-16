SELECT rdsadmin.rdsadmin_s3_tasks.download_from_s3(
 p_bucket_name => 'NAME OF THE BUCKET THAT CONTAINS THE DATA',
 p_s3_prefix => 'NAME OF THE FOLDER (well, S3 does not actually use folders, but prefixes) ON THE BUCKET THAT HOLDS THE DATA, don't forget the trailing slash/',
 p_directory_name => 'DATA_PUMP_DIR',
 p_decompression_format => 'GZIP'
) AS TASK_ID FROM DUAL;
