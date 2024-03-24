from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from helpers import utils
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging 
from sqlalchemy import create_engine
import re

from airflow_dbt.operators.dbt_operator import DbtRunOperator

load_dotenv()

CONNECTION_ID = "postgres"
DB_NAME = "etl_dbt_airflow"
SCHEMA_NAME = "postgres"
# The path to the dbt project
DBT_PROJECT_PATH = "/opt/airflow/dbt/airflowdbt"

# Fungsi untuk mendapatkan data dari Web
def extract_data_from_web():
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

# Fungsi untuk memuat data ke dalam tabel PostgreSQL
def load_to_postgres(**kwargs):
    # try:
    ti = kwargs['ti']
    tbl_pemain = ti.xcom_pull(task_ids='extract_data_from_web')
    # Konversi JSON ke DataFrame
    tbl_pemain_df = pd.DataFrame(tbl_pemain)
    tbl_pemain_df.insert(loc=0, column='id', value= tbl_pemain_df.reset_index().index + 1)
    
    # Buat koneksi ke PostgreSQL
    engine = create_engine(os.getenv('ENGINE_CONNECT'))
    # Tulis DataFrame ke dalam tabel PostgreSQL
    tbl_pemain_df.to_sql('tbl_pemain', engine, if_exists='replace', index=False)
# Definisikan default arguments untuk DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 25),
    'retries': 1,
}

# Inisialisasi DAG
dag = DAG(
    'scrap_load_data_to_postgres',
    # default_args=default_args,
    start_date=datetime.now(),
    description='ETL pipeline for Football API to PostgreSQL',
    # schedule_interval='@daily',
)


start = EmptyOperator(task_id='start', dag=dag)
end = EmptyOperator(task_id='end', dag=dag)

# Task untuk mendapatkan data dari API
get_data_task = PythonOperator(
    task_id='extract_data_from_web',
    python_callable=extract_data_from_web,
    dag=dag,
)

# Task untuk memuat data ke PostgreSQL
load_to_postgres_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    provide_context=True,
    dag=dag,
)

dbt_run_model_1 = DbtRunOperator(
        task_id="dbt_run_model_1",
        select="model_1",
        profiles_dir=DBT_PROJECT_PATH,
        dir=DBT_PROJECT_PATH, 
        dag=dag
    )

if __name__ == '__main__':
    # Mengatur dependensi antar task
    start >> get_data_task >> load_to_postgres_task >> dbt_run_model_1 >> end
