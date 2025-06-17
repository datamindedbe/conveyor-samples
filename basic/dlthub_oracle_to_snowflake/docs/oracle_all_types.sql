CREATE TABLE TPCH.all_data_types_demo (
    -- Numeric types
    num_number NUMBER,                     -- Variable numeric value
    num_number_precision NUMBER(10,2),     -- Number with precision and scale
    num_decimal DECIMAL(9,2),              -- Exact decimal (synonym for NUMBER(9,2))
    num_float BINARY_FLOAT,                -- 32-bit floating point
    num_float_explicit FLOAT(5),           -- Floating point with binary precision
    num_double BINARY_DOUBLE,              -- 64-bit floating point
    
    -- Character types
    char_col CHAR(10),                    -- Fixed-length character
    char_varchar2 VARCHAR2(100),           -- Variable-length character
    char_nchar NCHAR(10),                  -- Fixed-length Unicode character
    char_nvarchar2 NVARCHAR2(100),         -- Variable-length Unicode character
    
    -- Date and time types
    dt_date DATE,                          -- Date and time (to the second)
    dt_timestamp TIMESTAMP,                -- Date and time with fractional seconds
    dt_timestamp_tz TIMESTAMP WITH TIME ZONE, -- Timestamp with time zone
    dt_timestamp_ltz TIMESTAMP WITH LOCAL TIME ZONE, -- Timestamp with local time zone
    dt_interval_ym INTERVAL YEAR TO MONTH,  -- Interval in years and months
    dt_interval_ds INTERVAL DAY TO SECOND,  -- Interval in days and seconds
    
    -- Large object types
    lob_clob CLOB,                         -- Character large object
    lob_nclob NCLOB,                       -- Unicode character large object
    lob_blob BLOB,                         -- Binary large object
    lob_bfile BFILE,                       -- External binary file reference
    
    -- Raw and rowid types
    raw_raw RAW(10),                      -- Binary data
    rowid_rowid ROWID,                     -- Physical row identifier
    rowid_urowid UROWID,                   -- Universal row identifier
    
    -- Boolean type (simulated)
    bool_yn VARCHAR2(1) CHECK (bool_yn IN ('Y', 'N')) -- Simulated boolean
);

INSERT INTO TPCH.ALL_DATA_TYPES_DEMO (
    num_number,
    num_number_precision,
    num_decimal,
    num_float,
    num_float_explicit,
    num_double,
    char_col,
    char_varchar2,
    char_nchar,
    char_nvarchar2,
    dt_date,
    dt_timestamp,
    dt_timestamp_tz,
    dt_timestamp_ltz,
    dt_interval_ym,
    dt_interval_ds,
    lob_clob,
    lob_nclob,
    lob_blob,
    lob_bfile,
    raw_raw,
    xml_type,
    bool_yn
)
VALUES (
    12345,                              -- num_number
    12345.67,                           -- num_number_precision
    12345.67,                           -- num_decimal
    1.23,                               -- num_float
    1.2345,                             -- num_float_explicit
    12345.6789,                         -- num_double
    'FixedChar',                         -- char_char (padded to 10 chars)
    'Variable length string',           -- char_varchar2
    N'固定文本',                         -- char_nchar (Unicode)
    N'可变文本',                         -- char_nvarchar2 (Unicode)
    SYSDATE,                             -- dt_date (current date)
    SYSTIMESTAMP,                        -- dt_timestamp (current timestamp)
    SYSTIMESTAMP,                        -- dt_timestamp_tz (current timestamp with time zone)
    SYSTIMESTAMP,                        -- dt_timestamp_ltz (current timestamp with local time zone)
    INTERVAL '2-6' YEAR TO MONTH,        -- dt_interval_ym (2 years, 6 months)
    INTERVAL '5 12:30:15.123' DAY TO SECOND, -- dt_interval_ds (5 days, 12 hours, 30 minutes, 15.123 seconds)
    'This is a CLOB value',             -- lob_clob (Character large object)
    N'This is a NCLOB value',           -- lob_nclob (Unicode character large object)
    UTL_RAW.CAST_TO_RAW('This is a BLOB value'), -- lob_blob (Binary large object)
    BFILENAME('MY_DIR', 'example_file.txt'),
    HEXTORAW('DEADBEEFCAFEBABE'),       -- raw_raw (Binary data)
    XMLTYPE('<root><element>Value</element></root>'), -- xml_type (XML data)
    'Y'                                 -- bool_yn (Simulated boolean)
);

INSERT INTO TPCH.INTERNAL_YM_DEMO (dt_interval_ds) VALUES (INTERVAL '5 12:30:15.123' DAY TO SECOND);
ALTER TABLE TPCH.INTERNAL_YM_DEMO ADD dt_interval_ds INTERVAL DAY TO SECOND;
ALTER TABLE TPCH.INTERNAL_YM_DEMO DROP COLUMN dt_interval_ds;