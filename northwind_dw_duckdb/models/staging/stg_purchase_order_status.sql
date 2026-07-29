with source as (

    select * from {{ source('northwind_dw_duckdb', 'purchase_order_status') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
