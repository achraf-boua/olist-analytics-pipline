SELECT
    *
FROM
    {{ ref('stg_orders') }}
WHERE
    approved_at < ordered_at