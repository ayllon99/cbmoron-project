import pendulum
from airflow.operators.python import PythonOperator
import ztests.hello as helloo
from airflow import DAG
from airflow.datasets import Dataset, DatasetAlias
from airflow.decorators import task



"""with DAG(
    dag_id="FROTH",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["consumer", "dataset-alias"],
)as dag:
    task=PythonOperator(
        task_id="iddd",
        python_callable=helloo.hello,
        op_kwargs={'category':'champions','link':'hahaha.com'}
    )

    task"""