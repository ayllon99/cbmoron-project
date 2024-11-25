from datetime import datetime
from airflow.operators.python import PythonOperator
import new_match_day
from airflow import DAG
from airflow.utils.task_group import TaskGroup
import inserting_into_postgres
import insert_into_mongo
import results_scraper_good


with DAG(
    dag_id='new_matchday_dag',
    schedule=None,
    default_args={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 6)
    },) as dag:
    
    scraping_results = PythonOperator(
        task_id='scraping_results',
        python_callable=results_scraper_good.results_scraper,
        do_xcom_push=True
    )

    uploading_results = PythonOperator(
        task_id='results_insert_data',
        python_callable=results_scraper_good.inserting_to_postgres,
        op_kwargs={"aa": "{{ ti.xcom_pull(task_ids='evaluate_and_trigger',key='aa') }}"},
        do_xcom_push=True
    )

    scraping_info = PythonOperator(
        task_id='scraping_match_info',
        python_callable=new_match_day.match_day,
        do_xcom_push=True
    )

    with TaskGroup("uploading_match_data",tooltip="Task Group for inserting data into mongo and postgres") as uploading_info:
        
        upload_to_mongo = PythonOperator(
            task_id='upload_to_mongo',
            python_callable=insert_into_mongo.uploadtomongo,
            do_xcom_push=True
        )
        
        insert_into_postgres = PythonOperator(
            task_id='teams_match_stats_insert_data',
            python_callable=inserting_into_postgres.teams_match_stats_insert_data,
            do_xcom_push=True
        )
        
        insert_into_postgres = PythonOperator(
            task_id='match_partials_insert_data',
            python_callable=inserting_into_postgres.match_partials_insert_data,
            do_xcom_push=True
        )

        insert_into_postgres = PythonOperator(
            task_id='players_matches_stats_insert_data',
            python_callable=inserting_into_postgres.players_matches_stats_insert_data,
            do_xcom_push=True
        )

        insert_into_postgres = PythonOperator(
            task_id='shootings_insert_data',
            python_callable=inserting_into_postgres.shootings_insert_data,
            do_xcom_push=True
        )

        insert_into_postgres = PythonOperator(
            task_id='shooting_chart_availability_insert_data',
            python_callable=inserting_into_postgres.shooting_chart_availability_insert_data,
            do_xcom_push=True
        )


        

    scraping_results >> scraping_info >> uploading_info
    scraping_results >> uploading_results
