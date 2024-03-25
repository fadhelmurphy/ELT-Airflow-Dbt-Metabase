{{
config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
)
}}

SELECT
    posisi,
    MAX(harga) AS market_value_max
FROM
    tbl_pemain
GROUP BY
    posisi
ORDER BY
    market_value_max DESC