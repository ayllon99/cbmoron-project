from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.utils.task_group import TaskGroup


def printing():
    print('PRINTIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIING')



with DAG(
    dag_id='third_dag',
    schedule=None,
    default_args={
    'owner': 'airflow',
    'catchup' : False,
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 6)
    },) as dag:
    
    scraping_info = PythonOperator(
        task_id='scraping_match_info',
        python_callable=printing,
        do_xcom_push=True
    )

