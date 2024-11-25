from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import checking_new_results


with DAG(
    dag_id="check_if_new_results",
    schedule=None,
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2024, 11, 6)
    },
) as dag:

    evaluate_and_trigger = PythonOperator(
        task_id="evaluate_and_trigger",
        python_callable=checking_new_results.new_results
    )

    trigger_dag = TriggerDagRunOperator(
        task_id="trigger_dag",
        trigger_dag_id="third_dag",
        dag=dag
    )

    evaluate_and_trigger >> trigger_dag