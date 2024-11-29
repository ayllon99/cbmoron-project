from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.datasets import Dataset, DatasetAlias
import pendulum
from airflow.decorators import task



"""
with DAG(
    dag_id="dataset_alias_example_alias_producer",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["producer", "dataset-alias"],
):

    @task(outlets=[DatasetAlias("example-alias")])
    def produce_dataset_events_through_dataset_alias(*, outlet_events=None):
        bucket_name = "bucket"
        object_path = "my-task"
        extra_info = {"key1": "value1", "key2": "value2"}  # Add extra information
        dataset = Dataset(f"s3://{bucket_name}/{object_path}")
        dataset.extra = extra_info
        print(dataset)
        print(dataset.extra)
        outlet_events["example-alias"].add(dataset)
        

    produce_dataset_events_through_dataset_alias()

"""