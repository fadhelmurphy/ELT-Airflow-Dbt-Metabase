from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

def create_operator(task_type, **kwargs):
    if task_type == 'python':
        return PythonOperator(**kwargs)
    elif task_type == 'bash':
        return BashOperator(**kwargs)
    elif task_type == 'empty':
        return EmptyOperator(**kwargs)
    else:
        raise ValueError(f"Unsupported task type: {task_type}")
    
# from airflow_dbt.operators.dbt_operator import DbtRunOperator

# dbt_run_model_1 = DbtRunOperator(
#         task_id="data_modelling_with_DbtRunOperator",
#         select=SCHEMA_NAME,
#         profiles_dir=DBT_PROJECT_PATH,
#         dir=DBT_PROJECT_PATH, 
#         dag=dag
#     )