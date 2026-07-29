with source as (

    select * from {{ source('northwind_dw_duckdb', 'shippers') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
