from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import checking_new_results
from airflow.exceptions import AirflowFailException


def trigger_evaluator(ti):
    result=ti.xcom_pull(task_ids='evaluate_and_trigger',key='trigger_evaluator')
    if result==False:
        print('Result == False here the exception comes')
        raise AirflowFailException('---------------NO NEW MATCHES TO SCRAPE---------------')
    print('New matches to scrape, triggering next DAG...')

with DAG(
    dag_id="check_if_new_results",
    schedule_interval="@daily",
    catchup=False,
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2022, 11, 6)
    },
) as dag:

    evaluate_and_trigger = PythonOperator(
        task_id="evaluate_and_trigger",
        python_callable=checking_new_results.new_results
    )

    should_trigger = PythonOperator(
        task_id="should_trigger",
        python_callable=trigger_evaluator
    )

    trigger_dag_new_matchday = TriggerDagRunOperator(
        task_id="trigger_dag_new_matchday",
        trigger_dag_id="new_matchday_dag",
    )

    evaluate_and_trigger >> should_trigger>> trigger_dag_new_matchday