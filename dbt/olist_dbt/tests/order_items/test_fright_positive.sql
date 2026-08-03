select 
    *
from
    {{ ref('stg_order_items') }}
where
    freight_value < 0