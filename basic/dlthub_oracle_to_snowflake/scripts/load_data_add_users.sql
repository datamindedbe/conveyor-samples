--------------------------------------------------------------------------------
-- Initializes the TPC-H schema, loads data from an external S3 bucket, applies the indices and constraints, and finally creates a user for dltHub.
--------------------------------------------------------------------------------

-- 1. Initialize the TPC-H schema
---------------------------------

CREATE USER tpch IDENTIFIED BY tpch;

GRANT CREATE SESSION,
      CREATE TABLE,
      UNLIMITED TABLESPACE
    TO tpch;


GRANT READ ON DIRECTORY DATA_PUMP_DIR TO tpch;

-- 1.4.1
--  per 1.4.2.1  all table columns may be defined NOT NULL

CREATE TABLE tpch.ext_part
(
    p_partkey       NUMBER(10, 0),
    p_name          VARCHAR2(55),
    p_mfgr          CHAR(25),
    p_brand         CHAR(10),
    p_type          VARCHAR2(25),
    p_size          INTEGER,
    p_container     CHAR(10),
    p_retailprice   NUMBER,
    p_comment       VARCHAR2(23)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('part.tbl'));

CREATE TABLE tpch.part
(
    p_partkey       NUMBER(10, 0) NOT NULL,
    p_name          VARCHAR2(55) NOT NULL,
    p_mfgr          CHAR(25) NOT NULL,
    p_brand         CHAR(10) NOT NULL,
    p_type          VARCHAR2(25) NOT NULL,
    p_size          INTEGER NOT NULL,
    p_container     CHAR(10) NOT NULL,
    p_retailprice   NUMBER NOT NULL,
    p_comment       VARCHAR2(23) NOT NULL
);


CREATE TABLE tpch.ext_supplier
(
    s_suppkey     NUMBER(10, 0),
    s_name        CHAR(25),
    s_address     VARCHAR2(40),
    s_nationkey   NUMBER(10, 0),
    s_phone       CHAR(15),
    s_acctbal     NUMBER,
    s_comment     VARCHAR2(101)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('supplier.tbl'));

CREATE TABLE tpch.supplier
(
    s_suppkey     NUMBER(10, 0) NOT NULL,
    s_name        CHAR(25) NOT NULL,
    s_address     VARCHAR2(40) NOT NULL,
    s_nationkey   NUMBER(10, 0) NOT NULL,
    s_phone       CHAR(15) NOT NULL,
    s_acctbal     NUMBER NOT NULL,
    s_comment     VARCHAR2(101) NOT NULL
);

CREATE TABLE tpch.ext_partsupp
(
    ps_partkey      NUMBER(10, 0),
    ps_suppkey      NUMBER(10, 0),
    ps_availqty     INTEGER,
    ps_supplycost   NUMBER,
    ps_comment      VARCHAR2(199)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('partsupp.tbl'));

CREATE TABLE tpch.partsupp
(
    ps_partkey      NUMBER(10, 0) NOT NULL,
    ps_suppkey      NUMBER(10, 0) NOT NULL,
    ps_availqty     INTEGER NOT NULL,
    ps_supplycost   NUMBER NOT NULL,
    ps_comment      VARCHAR2(199) NOT NULL
);

CREATE TABLE tpch.ext_customer
(
    c_custkey      NUMBER(10, 0),
    c_name         VARCHAR2(25),
    c_address      VARCHAR2(40),
    c_nationkey    NUMBER(10, 0),
    c_phone        CHAR(15),
    c_acctbal      NUMBER,
    c_mktsegment   CHAR(10),
    c_comment      VARCHAR2(117)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('customer.tbl'));

CREATE TABLE tpch.customer
(
    c_custkey      NUMBER(10, 0) NOT NULL,
    c_name         VARCHAR2(25) NOT NULL,
    c_address      VARCHAR2(40) NOT NULL,
    c_nationkey    NUMBER(10, 0) NOT NULL,
    c_phone        CHAR(15) NOT NULL,
    c_acctbal      NUMBER NOT NULL,
    c_mktsegment   CHAR(10) NOT NULL,
    c_comment      VARCHAR2(117) NOT NULL
);

-- read date values as yyyy-mm-dd text

CREATE TABLE tpch.ext_orders
(
    o_orderkey        NUMBER(10, 0),
    o_custkey         NUMBER(10, 0),
    o_orderstatus     CHAR(1),
    o_totalprice      NUMBER,
    o_orderdate       CHAR(10),
    o_orderpriority   CHAR(15),
    o_clerk           CHAR(15),
    o_shippriority    INTEGER,
    o_comment         VARCHAR2(79)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('orders.tbl'));

CREATE TABLE tpch.orders
(
    o_orderkey        NUMBER(11, 0) NOT NULL,
    o_custkey         NUMBER(10, 0) NOT NULL,
    o_orderstatus     CHAR(1) NOT NULL,
    o_totalprice      NUMBER NOT NULL,
    o_orderdate       DATE NOT NULL,
    o_orderpriority   CHAR(15) NOT NULL,
    o_clerk           CHAR(15) NOT NULL,
    o_shippriority    INTEGER NOT NULL,
    o_comment         VARCHAR2(79) NOT NULL
);

-- read date values as yyyy-mm-dd text

CREATE TABLE tpch.ext_lineitem
(
    l_orderkey        NUMBER(10, 0),
    l_partkey         NUMBER(10, 0),
    l_suppkey         NUMBER(10, 0),
    l_linenumber      INTEGER,
    l_quantity        NUMBER,
    l_extendedprice   NUMBER,
    l_discount        NUMBER,
    l_tax             NUMBER,
    l_returnflag      CHAR(1),
    l_linestatus      CHAR(1),
    l_shipdate        CHAR(10),
    l_commitdate      CHAR(10),
    l_receiptdate     CHAR(10),
    l_shipinstruct    CHAR(25),
    l_shipmode        CHAR(10),
    l_comment         VARCHAR2(44)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('lineitem.tbl'));

CREATE TABLE tpch.lineitem
(
    l_orderkey        NUMBER(10, 0),
    l_partkey         NUMBER(10, 0),
    l_suppkey         NUMBER(10, 0),
    l_linenumber      INTEGER,
    l_quantity        NUMBER,
    l_extendedprice   NUMBER,
    l_discount        NUMBER,
    l_tax             NUMBER,
    l_returnflag      CHAR(1),
    l_linestatus      CHAR(1),
    l_shipdate        DATE,
    l_commitdate      DATE,
    l_receiptdate     DATE,
    l_shipinstruct    CHAR(25),
    l_shipmode        CHAR(10),
    l_comment         VARCHAR2(44)
);

CREATE TABLE tpch.ext_nation
(
    n_nationkey   NUMBER(10, 0),
    n_name        CHAR(25),
    n_regionkey   NUMBER(10, 0),
    n_comment     VARCHAR(152)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('nation.tbl'));

CREATE TABLE tpch.nation
(
    n_nationkey   NUMBER(10, 0),
    n_name        CHAR(25),
    n_regionkey   NUMBER(10, 0),
    n_comment     VARCHAR(152)
);

CREATE TABLE tpch.ext_region
(
    r_regionkey   NUMBER(10, 0),
    r_name        CHAR(25),
    r_comment     VARCHAR(152)
)
ORGANIZATION EXTERNAL
    (TYPE oracle_loader
          DEFAULT DIRECTORY DATA_PUMP_DIR
              ACCESS PARAMETERS (
                  FIELDS
                      TERMINATED BY '|'
                  MISSING FIELD VALUES ARE NULL
              )
          LOCATION('region.tbl'));

CREATE TABLE tpch.region
(
    r_regionkey   NUMBER(10, 0),
    r_name        CHAR(25),
    r_comment     VARCHAR(152)
);


-- 2. Loads the data from the external tables
---------------------------------------------

TRUNCATE TABLE tpch.part;
TRUNCATE TABLE tpch.supplier;
TRUNCATE TABLE tpch.partsupp;
TRUNCATE TABLE tpch.customer;
TRUNCATE TABLE tpch.orders;
TRUNCATE TABLE tpch.lineitem;
TRUNCATE TABLE tpch.nation;
TRUNCATE TABLE tpch.region;

ALTER SESSION SET nls_date_format='YYYY-MM-DD';

INSERT /*+ APPEND */ INTO  tpch.part     SELECT * FROM tpch.ext_part;
INSERT /*+ APPEND */ INTO  tpch.supplier SELECT * FROM tpch.ext_supplier;
INSERT /*+ APPEND */ INTO  tpch.partsupp SELECT * FROM tpch.ext_partsupp;
INSERT /*+ APPEND */ INTO  tpch.customer SELECT * FROM tpch.ext_customer;
INSERT /*+ APPEND */ INTO  tpch.orders   SELECT * FROM tpch.ext_orders;
INSERT /*+ APPEND */ INTO  tpch.lineitem SELECT * FROM tpch.ext_lineitem;
INSERT /*+ APPEND */ INTO  tpch.nation   SELECT * FROM tpch.ext_nation;
INSERT /*+ APPEND */ INTO  tpch.region   SELECT * FROM tpch.ext_region;

-- 3. add indices and constraints
---------------------------------

ALTER TABLE tpch.part
    ADD CONSTRAINT pk_part PRIMARY KEY(p_partkey);

ALTER TABLE tpch.supplier
    ADD CONSTRAINT pk_supplier PRIMARY KEY(s_suppkey);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT pk_partsupp PRIMARY KEY(ps_partkey, ps_suppkey);

ALTER TABLE tpch.customer
    ADD CONSTRAINT pk_customer PRIMARY KEY(c_custkey);

ALTER TABLE tpch.orders
    ADD CONSTRAINT pk_orders PRIMARY KEY(o_orderkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT pk_lineitem PRIMARY KEY(l_linenumber, l_orderkey);

ALTER TABLE tpch.nation
    ADD CONSTRAINT pk_nation PRIMARY KEY(n_nationkey);

ALTER TABLE tpch.region
    ADD CONSTRAINT pk_region PRIMARY KEY(r_regionkey);

-- 1.4.2.3

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT fk_partsupp_part FOREIGN KEY(ps_partkey) REFERENCES tpch.part(p_partkey);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT fk_partsupp_supplier FOREIGN KEY(ps_suppkey) REFERENCES tpch.supplier(s_suppkey);

ALTER TABLE tpch.customer
    ADD CONSTRAINT fk_customer_nation FOREIGN KEY(c_nationkey) REFERENCES tpch.nation(n_nationkey);

ALTER TABLE tpch.orders
    ADD CONSTRAINT fk_orders_customer FOREIGN KEY(o_custkey) REFERENCES tpch.customer(c_custkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_order FOREIGN KEY(l_orderkey) REFERENCES tpch.orders(o_orderkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_part FOREIGN KEY(l_partkey) REFERENCES tpch.part(p_partkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_supplier FOREIGN KEY(l_suppkey) REFERENCES tpch.supplier(s_suppkey);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT fk_lineitem_partsupp FOREIGN KEY(l_partkey, l_suppkey)
        REFERENCES tpch.partsupp(ps_partkey, ps_suppkey);

-- 1.4.2.4 - 1

ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_partkey CHECK(p_partkey >= 0);

ALTER TABLE tpch.supplier
    ADD CONSTRAINT chk_supplier_suppkey CHECK(s_suppkey >= 0);

ALTER TABLE tpch.customer
    ADD CONSTRAINT chk_customer_custkey CHECK(c_custkey >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_partkey CHECK(ps_partkey >= 0);

ALTER TABLE tpch.region
    ADD CONSTRAINT chk_region_regionkey CHECK(r_regionkey >= 0);

ALTER TABLE tpch.nation
    ADD CONSTRAINT chk_nation_nationkey CHECK(n_nationkey >= 0);

-- 1.4.2.4 - 2

ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_size CHECK(p_size >= 0);

ALTER TABLE tpch.part
    ADD CONSTRAINT chk_part_retailprice CHECK(p_retailprice >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_availqty CHECK(ps_availqty >= 0);

ALTER TABLE tpch.partsupp
    ADD CONSTRAINT chk_partsupp_supplycost CHECK(ps_supplycost >= 0);

ALTER TABLE tpch.orders
    ADD CONSTRAINT chk_orders_totalprice CHECK(o_totalprice >= 0);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_quantity CHECK(l_quantity >= 0);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_extendedprice CHECK(l_extendedprice >= 1);

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_tax CHECK(l_tax >= 0);

-- 1.4.2.4 - 3

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_discount CHECK(l_discount >= 0.00 AND l_discount <= 1.00);

-- 1.4.2.4 - 4

ALTER TABLE tpch.lineitem
    ADD CONSTRAINT chk_lineitem_ship_rcpt CHECK(l_shipdate <= l_receiptdate);

-- 4. create the role that dltHub will use.
-------------------------------------------

CREATE ROLE read_only_role;

BEGIN
  FOR x IN (SELECT table_name FROM dba_tables WHERE owner='TPCH' AND tablespace_name = 'USERS')
  LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON TPCH.' || x.table_name ||
                                  ' TO read_only_role';
  END LOOP;
END;


CREATE USER dlthub IDENTIFIED BY dltpass;
GRANT CREATE SESSION TO dlthub;
GRANT read_only_role TO dlthub;
