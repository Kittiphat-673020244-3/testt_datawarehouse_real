with source as (

    select * from {{ source('northwind_dw_duckdb', 'order_details') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
