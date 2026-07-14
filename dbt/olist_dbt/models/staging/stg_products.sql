-- ================================================================
-- mdele : stg_products
-- Description : Modèle de staging pour la table des produits.
-- Il lit la table brute raw_products depuis la couche bronze (RAW),
-- nettoie les types de données, renomme les colonnes pour plus de cohérence.
-- Sortie : OLIST_DB.STAGING.STG_PRODUCTS (vue)
-- ================================================================

with src_products as (

    select * from {{ source('olist_raw', 'products') }}

),

stg_products as (

#========================================================================================
# les colonnes product_name_lenght, product_description_lenght et product_photos_qty,
# peuvent être utilisés pour voir par exemple si une description plus courte ou plus 
# longue a un impact sur les ventes.
#========================================================================================
    select
        product_id,
        product_category_name as category_name,
        cast(product_name_lenght as integer) as product_name_lenght,
        cast(product_description_lenght as integer) as product_description_lenght,
        cast(product_photos_qty as integer) as product_photos_quantity,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm

    from src_products

)

select * from stg_products