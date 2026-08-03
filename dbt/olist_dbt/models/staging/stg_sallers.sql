-------------------------

-------------------------

with src_sallers as (

    select 
        *
    from
        {{ source('olist_raw', 'sellers') }}

),

stg_sallers as (

    select
        seller_id,
        cast(seller_zip_code_prefix as string) as zip_code_prefix,
        initcap(seller_city) as seller_city,
        seller_state

    from src_sallers

)

select * from stg_sallers