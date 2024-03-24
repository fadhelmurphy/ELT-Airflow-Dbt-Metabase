FROM apache/airflow:latest


# Switch to the airflow user
USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt