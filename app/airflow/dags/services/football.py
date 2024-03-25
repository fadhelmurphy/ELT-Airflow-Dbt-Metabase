from helpers import utils
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# Fungsi untuk mendapatkan data dari Web
def get_extract_transfermarkt():
    url = "https://www.transfermarkt.co.id/manchester-united/kader/verein/985/saison_id/2023/plus/1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    list_pemain = []

    if response.status_code == 200:
        print("Sukses!")
        soup = BeautifulSoup(response.content, "html.parser")

        get_table = soup.find_all("tbody")[1]

        for item in get_table.find_all("tr"):
            item_pemain = {}
            first_col = item.find("td", class_="posrela")
            second_col = item.find_all("td", class_="zentriert")
            
            if first_col and second_col:
                item_pemain['nomor_punggung'] = str(np.ravel(second_col[0])[0])
                item_pemain['nama'] = first_col.find_all("td")[1].text.strip()
                item_pemain['posisi'] = first_col.find_all("td")[2].text.strip()
                harga = item.find("td", class_="rechts hauptlink").find("a").text.strip()
                item_pemain['harga_text'] = harga
                item_pemain['harga'] = utils.convert_to_billion(harga)
                tanggal_umur = second_col[1].text.strip()
                item_pemain['kelahiran'] = utils.extract_date_tanggal_umur(tanggal_umur)
                umur = re.search(r'\((\d+)\)', tanggal_umur).group(1)
                umur = int(umur)
                item_pemain['umur'] = umur
                item_pemain['tinggi'] = second_col[3].text.strip()
                item_pemain['kaki_dominan'] = second_col[4].text.strip()
                bergabung = second_col[5].text.strip()
                item_pemain['bergabung'] = utils.extract_date(bergabung)
                kontrak = second_col[7].text.strip()
                item_pemain['kontrak'] = utils.extract_date(kontrak) if kontrak != "-" else None
                item_pemain['klub_sebelumnya'] = second_col[6].find("img").get("title")
                countries = [country.get("title") for country in second_col[2].find_all("img")]
                if len(countries) > 1:
                    for country in countries:
                        second_item_pemain = item_pemain.copy()
                        second_item_pemain['negara'] = country
                        list_pemain.append(second_item_pemain)
                elif len(countries) == 1:
                    item_pemain['negara'] = countries[0]
                    list_pemain.append(item_pemain)

        print("Semua data pemain berhasil di scraping!")
    else:
        print("Gagal:", response.status_code)
    
    return list_pemain
