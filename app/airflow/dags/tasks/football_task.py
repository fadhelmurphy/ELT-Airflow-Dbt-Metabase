
from dotenv import load_dotenv
from services import football
from db.postgres import engine as psql_engine
import os
from helpers.operators import create_operator
from datetime import datetime
from airflow import DAG
from datetime import datetime
import pandas as pd

load_dotenv()

DBT_PROJECT_PATH="/opt/airflow/dbt/airflowdbt"

# Definisikan default arguments untuk DAG
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 3, 25),
#     'retries': 1,
# }

def load_to_postgres(**kwargs):
    """
    Load data to PostgreSQL.

    Args:
        psql_engine: SQLAlchemy engine for PostgreSQL connection.
        **kwargs: Keyword arguments provided by Airflow.

    Returns:
        None
    """
    ti = kwargs['ti']
    tbl_pemain = ti.xcom_pull(task_ids='extract_data_from_web')
    tbl_pemain_df = pd.DataFrame(tbl_pemain)
    tbl_pemain_df.insert(loc=0, column='id', value= tbl_pemain_df.reset_index().index + 1)
    
    tbl_pemain_df.to_sql('tbl_pemain', psql_engine, if_exists='replace', index=False)



# Inisialisasi DAG
dag = DAG(
    'scrap_load_data_to_postgres',
    # default_args=default_args,
    start_date=datetime.now(),
    description='ELT pipeline for Football Website to PostgreSQL',
    # schedule_interval='@daily',
)


start = create_operator(
    task_type='empty',task_id='start_ELT_cuy', dag=dag)
end = create_operator(
    task_type='empty',task_id='end_ELT_cuy', dag=dag)

# Task untuk mendapatkan data dari API
get_data_task = create_operator(
    task_type='python',
    task_id='extract_data_from_web',
    python_callable=football.get_extract_transfermarkt,
    dag=dag,
)

# Task untuk memuat data ke PostgreSQL
load_to_postgres_task = create_operator(
    task_type='python',
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    provide_context=True,
    dag=dag,
)


  # run dbt run to do the data modelling.
data_modelling = create_operator(
    task_type='bash',
    task_id='dbt_data_modelling',
    bash_command= f"cd {DBT_PROJECT_PATH} && dbt run",
    dag=dag,
  )

