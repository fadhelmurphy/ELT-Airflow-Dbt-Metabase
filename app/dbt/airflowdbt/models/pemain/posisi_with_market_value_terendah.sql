{{
config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
)
}}

SELECT
    posisi,
    MIN(harga) AS market_value_min
FROM
    tbl_pemain
GROUP BY
    posisi
ORDER BY
    market_value_min ASC