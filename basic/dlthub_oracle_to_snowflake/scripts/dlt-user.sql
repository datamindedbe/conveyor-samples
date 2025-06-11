-- create the role that dlthub will use. To be executed after the tables have been provisioned (tpc-h-schema-init).

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
