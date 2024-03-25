{{
config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply',
)
}}


SELECT nama, kontrak, harga_text, harga,
    CASE
        WHEN bergabung IS NOT NULL THEN 
            CONCAT(
                EXTRACT(YEAR FROM AGE(CURRENT_DATE, bergabung)), ' tahun ',
                EXTRACT(MONTH FROM AGE(CURRENT_DATE, bergabung)), ' bulan'
            )
        ELSE NULL
    END as lama_bermain_text,
    (EXTRACT(YEAR FROM AGE(CURRENT_DATE, bergabung)) * 12 + EXTRACT(MONTH FROM AGE(CURRENT_DATE, bergabung))) as lama_bermain_bulan
FROM tbl_pemain
WHERE 
	kontrak <= CURRENT_DATE + INTERVAL '1 year'
group by nama, kontrak, harga_text, harga, lama_bermain_text, lama_bermain_bulan
order by harga desc