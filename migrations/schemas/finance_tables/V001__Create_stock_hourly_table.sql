CREATE TABLE IF NOT EXISTS finance.stock_hourly_raw
(
    id              varchar(36)                 not null primary key,
    ticker          varchar(6)                  not null,
    updated_at      timestamp default now()     not null,
    ts              bigint                      not null,
    dt              date                        not null,
    price           float,
    change          float,
    prc_change      float,
    volume          integer,
    low             float,
    high            float
);

ALTER DEFAULT PRIVILEGES IN SCHEMA finance GRANT ALL PRIVILEGES ON TABLES TO admin_group;
ALTER DEFAULT PRIVILEGES IN SCHEMA finance GRANT USAGE ON SEQUENCES TO admin_group;

GRANT USAGE ON SCHEMA finance TO GROUP etl_group;
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA finance TO GROUP etl_group;

GRANT USAGE ON SCHEMA finance TO GROUP readonly_group;
GRANT SELECT ON ALL TABLES IN SCHEMA finance TO GROUP readonly_group;