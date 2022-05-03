CREATE TABLE IF NOT EXISTS finance.exchange_rates
(
    dt              date                        not null primary key,
    updated_dt      date                        not null,
    base_currency   varchar(3)                  not null,
    target_currency varchar(3)                  not null,
    rate            float
);

ALTER DEFAULT PRIVILEGES IN SCHEMA finance GRANT ALL PRIVILEGES ON TABLES TO admin_group;
ALTER DEFAULT PRIVILEGES IN SCHEMA finance GRANT USAGE ON SEQUENCES TO admin_group;

GRANT USAGE ON SCHEMA finance TO GROUP etl_group;
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA finance TO GROUP etl_group;

GRANT USAGE ON SCHEMA finance TO GROUP readonly_group;
GRANT SELECT ON ALL TABLES IN SCHEMA finance TO GROUP readonly_group;