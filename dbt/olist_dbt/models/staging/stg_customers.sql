-- =========================================================
-- Modèle de staging : vendeurs
-- =========================================================
-- Lit la table brute raw_customers depuis la couche bronze (RAW),
-- nettoie les types de données, renomme les colonnes pour plus
-- de cohérence .
-- Sortie : OLIST_DB.STAGING.STG_CUSTOMERS (vue)
-- =========================================================

-- CTE 1 : lecture de la source brute 
with customers_source as (

    select * from {{ source ('olist_raw', 'customers') }}
    
),

-- CTE 2 : typage et renommage des colonnes
stg_customers as (

    select
        customer_id, # Identifiant du client pour une commande
        customer_unique_id, # Identifiant du client pour toute les commandes
        cast(customer_zip_code_prefix as string) as customer_zip_code,
        customer_city,
        customer_state
    from customers_source

)

-- Sortie finale du modèle
select * from stg_customers


