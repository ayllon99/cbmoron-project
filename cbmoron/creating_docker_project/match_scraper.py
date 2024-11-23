from datetime import datetime
from airflow.operators.python import PythonOperator
import new_match_day
from airflow import DAG
from airflow.utils.task_group import TaskGroup
import inserting_into_postgres
import insert_into_mongo


with DAG(
    dag_id='match_scraper',
    schedule=None,
    default_args={
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 6)
    },) as dag:
    
    scraping_info = PythonOperator(
        task_id='scraping_info',
        python_callable=new_match_day.match_day,
        do_xcom_push=True
    )

    with TaskGroup("uploading_data",tooltip="Task Group for inserting data into mongo and postgres") as uploading_info:
        
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


        

    scraping_info >> uploading_info

