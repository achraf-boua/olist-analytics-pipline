SELECT
    * 
FROM 
    {{ref('stg_orders')}}
WHERE
    ordered_at > CURRENT_TIMESTAMP
