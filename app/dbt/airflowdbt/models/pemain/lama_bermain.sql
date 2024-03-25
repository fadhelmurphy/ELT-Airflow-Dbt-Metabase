{{
config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
)
}}

SELECT
    distinct nama,
    posisi,
    (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM kelahiran)) as umur,
    harga_text,
    harga,
    bergabung,
    kontrak,
    CASE
        WHEN bergabung IS NOT NULL THEN 
            CONCAT(
                EXTRACT(YEAR FROM AGE(CURRENT_DATE, bergabung)), ' tahun ',
                EXTRACT(MONTH FROM AGE(CURRENT_DATE, bergabung)), ' bulan'
            )
        ELSE NULL
    END as lama_bermain_text,
    (EXTRACT(YEAR FROM AGE(CURRENT_DATE, bergabung)) * 12 + EXTRACT(MONTH FROM AGE(CURRENT_DATE, bergabung))) as lama_bermain_bulan
FROM
    tbl_pemain
ORDER BY
    umur ASC
	,lama_bermain_bulan desc;
