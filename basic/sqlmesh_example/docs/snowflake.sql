-- This code is used to as reference to set up the Snowflake environment for SQLMesh using terraform
-- Suggested in sqlmesh documentation 
-- https://sqlmesh.readthedocs.io/en/stable/integrations/engines/snowflake/#access-control-permissions

USE ROLE useradmin; -- This code requires USERADMIN privileges or higher

CREATE ROLE sqlmesh; -- Create role for permissions
CREATE DATABASE demo_db; -- Create database for SQLMesh to use (omit if database already exists)

GRANT USAGE ON WAREHOUSE compute_wh TO ROLE sqlmesh; -- Can use warehouse
GRANT USAGE ON DATABASE demo_db TO ROLE sqlmesh; -- Can use database

GRANT CREATE SCHEMA ON DATABASE demo_db TO ROLE sqlmesh; -- Can create SCHEMAs in database
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE demo_db TO ROLE sqlmesh; -- Can use schemas it creates
GRANT CREATE TABLE ON FUTURE SCHEMAS IN DATABASE demo_db TO ROLE sqlmesh; -- Can create TABLEs in schemas
GRANT CREATE VIEW ON FUTURE SCHEMAS IN DATABASE demo_db TO ROLE sqlmesh; -- Can create VIEWs in schemas
GRANT SELECT, INSERT, TRUNCATE, UPDATE, DELETE ON FUTURE TABLES IN DATABASE demo_db TO ROLE sqlmesh; -- Can SELECT and modify TABLEs in schemas
GRANT REFERENCES, SELECT ON FUTURE VIEWS IN DATABASE demo_db TO ROLE sqlmesh; -- Can SELECT and modify VIEWs in schemas

GRANT ROLE sqlmesh TO USER demo_user; -- Grant role to user
ALTER USER demo_user SET DEFAULT ROLE = sqlmesh; -- Make role user's default role