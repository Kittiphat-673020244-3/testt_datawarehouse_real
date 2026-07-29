with source as (

    select * from {{ source('northwind_dw_duckdb', 'strings') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
