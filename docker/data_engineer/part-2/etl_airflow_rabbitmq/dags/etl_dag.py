from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('etl_pipeline',
         default_args=default_args,
         schedule_interval='@hourly',
         catchup=False) as dag:

    run_etl = BashOperator(
        task_id='run_etl_container',
        bash_command='docker-compose run --rm etl'
    )
