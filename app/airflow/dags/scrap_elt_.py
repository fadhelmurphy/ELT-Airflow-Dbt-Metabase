from tasks import football_task
from airflow.models.baseoperator import chain

with football_task.dag:

    chain(football_task.start, 
            football_task.get_data_task, 
            football_task.load_to_postgres_task,
            football_task.data_modelling,
            football_task.end
            )