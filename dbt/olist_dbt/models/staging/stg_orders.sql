-- =========================================================
-- Modèle de staging : commandes
-- =========================================================
-- Lit la table brute raw_orders depuis la couche bronze (RAW),
-- nettoie les types de données, renomme les colonnes pour plus
-- de cohérence .
-- 
-- Sortie : OLIST_DB.STAGING.STG_ORDERS (vue)
-- =========================================================

-- CTE 1 : lecture de la source brute
with orders_source as (

    select * from {{ source('olist_raw', 'orders') }}

),

-- CTE 2 : typage et renommage des colonnes
stg_orders as (

    select
        -- Identifiants
        order_id,
        customer_id,
        order_status,

        -- Timestamps : on convertit les strings du CSV en vrais types timestamp
        cast(order_purchase_timestamp     as timestamp) as ordered_at,
        cast(order_approved_at            as timestamp) as approved_at,
        cast(order_delivered_carrier_date as timestamp) as shipped_at,
        cast(order_delivered_customer_date as timestamp) as delivered_at,
        cast(order_estimated_delivery_date as timestamp) as estimated_delivery_at

    from orders_source
)

-- Sortie finale du modèle
select * from stg_orders