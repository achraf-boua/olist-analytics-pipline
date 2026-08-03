select 
    *
from
    {{ ref('stg_orders') }}
where 
    delivered_at < ordered_at