import pendulum

from airflow import DAG
from airflow.datasets import Dataset, DatasetAlias
from airflow.decorators import task


"""
with DAG(
    dag_id="dataset_alias_example_alias_consumer",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[DatasetAlias("example-alias")],
    catchup=False,
    tags=["consumer", "dataset-alias"],
):

    @task(inlets=[DatasetAlias("example-alias")])
    def consume_dataset_event_from_dataset_alias(*, inlet_events=None):
        for event in inlet_events[DatasetAlias("example-alias")]:
            print(event)
            print(event.extra)

    consume_dataset_event_from_dataset_alias()"""