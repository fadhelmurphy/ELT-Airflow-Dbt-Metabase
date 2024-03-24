SELECT * FROM public.tbl_pemain
LIMIT 100;

SELECT negara, sum(harga) FROM public.tbl_pemain
	group by negara
	order by sum(harga) desc
LIMIT 100;

SELECT id, nama, kontrak, harga_text
FROM tbl_pemain
WHERE 
	kontrak <= CURRENT_DATE + INTERVAL '1 year';

SELECT nama, kontrak, harga_text, harga
FROM tbl_pemain
WHERE 
	kontrak <= CURRENT_DATE + INTERVAL '1 year'
group by nama, kontrak, harga_text, harga
order by harga desc


