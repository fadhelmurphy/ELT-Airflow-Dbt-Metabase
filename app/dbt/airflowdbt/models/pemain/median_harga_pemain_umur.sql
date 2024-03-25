{{
config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
)
}}

SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY harga) AS median_price,
    umur
FROM
    (SELECT
        EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM kelahiran) as umur,
        harga
    FROM
        tbl_pemain) AS subquery
GROUP BY
    umur
ORDER BY
    umur;