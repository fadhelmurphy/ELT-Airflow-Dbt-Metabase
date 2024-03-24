from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
from helpers import utils
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging 
from sqlalchemy import create_engine, exc

load_dotenv()

# Fungsi untuk mendapatkan data dari API menggunakan curl
def get_data_from_api():
    headers = {
        'X-Auth-Token': os.getenv('AIRFLOW_FOOTBALL_API_KEY')
    }
    response = requests.get('https://api.football-data.org/v4/teams/66/', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from the API")
        return None

# Fungsi untuk mentransform data dan membuat tabel
def transform_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='get_data_from_api')
    # Extracting player details
    players = data['squad']
    
    # Membuat DataFrame untuk tbl_pemain
    tbl_pemain_df = pd.DataFrame(columns=['id', 'name', 'position', 'age', 'country_name'])
    for player in players:
        tbl_pemain_df = tbl_pemain_df._append({
            'id': player['id'],
            'name': player['name'],
            'position': player['position'],
            'age': utils.hitung_umur(player['dateOfBirth']),
            'country_name': player['nationality']
        }, ignore_index=True)
    
    # Membuat DataFrame tbl_country
    tbl_nationality_df = tbl_pemain_df['country_name'].value_counts().reset_index()
    tbl_nationality_df.columns = ['country_name', 'players_cnt']
    
    # Menghitung jumlah pemain berdasarkan posisi
    tbl_position_df = pd.DataFrame(tbl_pemain_df['position'].value_counts()).reset_index()
    tbl_position_df.columns = ['position', 'players_cnt']
    
    return tbl_pemain_df.to_json(), tbl_nationality_df.to_json(), tbl_position_df.to_json()

# Fungsi untuk memeriksa dan membuat database jika belum ada
def check_and_create_database(engine, database_name):
    # Coba membuat database
    try:
        engine.execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' berhasil dibuat.")
    except exc.ProgrammingError as e:
        print(f"Database '{database_name}' sudah ada.")

# Fungsi untuk memuat data ke dalam tabel PostgreSQL
def load_to_postgres(**kwargs):
    # try:
    ti = kwargs['ti']
    tbl_pemain_json, tbl_nationality_json, tbl_position_json = ti.xcom_pull(task_ids='transform_data')
    # Konversi JSON ke DataFrame
    tbl_pemain_df = pd.read_json(tbl_pemain_json)
    tbl_nationality_df = pd.read_json(tbl_nationality_json)
    tbl_position_df = pd.read_json(tbl_position_json)
    
    # Buat koneksi ke PostgreSQL
    engine = create_engine(os.getenv('ENGINE_CONNECT'))
    
    # # Ambil nama database dari URI koneksi
    # database_name = engine.url.database
    
    # # Periksa dan buat database jika belum ada
    # check_and_create_database(engine, database_name)
    
    # Tulis DataFrame ke dalam tabel PostgreSQL
    tbl_pemain_df.to_sql('tbl_pemain', engine, if_exists='replace', index=False)
    tbl_nationality_df.to_sql('tbl_nationality', engine, if_exists='replace', index=False)
    tbl_position_df.to_sql('tbl_position', engine, if_exists='replace', index=False)
    # except Exception as e:
    #     logging.error(e, "Something went wrong")
# Definisikan default arguments untuk DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 25),
    'retries': 1,
}

# Inisialisasi DAG
dag = DAG(
    'load_data_to_postgres',
    # default_args=default_args,
    start_date=datetime.now(),
    description='ETL pipeline for Football API to PostgreSQL',
    schedule_interval='@daily',
)

# Task untuk mendapatkan data dari API
get_data_task = PythonOperator(
    task_id='get_data_from_api',
    python_callable=get_data_from_api,
    dag=dag,
)

# Task untuk mentransform data
transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

# Task untuk memuat data ke PostgreSQL
load_to_postgres_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    provide_context=True,
    dag=dag,
)

if __name__ == '__main__':
    # Mengatur dependensi antar task
    get_data_task >> transform_data_task >> load_to_postgres_task
