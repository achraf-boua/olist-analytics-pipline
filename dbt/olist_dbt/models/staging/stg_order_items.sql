-------------------------
------------------------

with src_order_items as (

    select 
        *
    from
        {{ source('olist_raw', 'order_items') }}

),

stg_order_items as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        cast(shipping_limit_date as timestamp) as shipping_limit_date,
        cast(price as float) as price,
        cast(freight_value as float) as freight_value

    from src_order_items

)

select * from stg_order_items