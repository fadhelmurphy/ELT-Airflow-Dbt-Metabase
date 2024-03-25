{{
config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
)
}}

SELECT
    negara,
    SUM(harga) AS total_market_value
FROM
    tbl_pemain
GROUP BY
    negara