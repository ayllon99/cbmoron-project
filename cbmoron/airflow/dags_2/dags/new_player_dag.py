from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
import checking_new_players
import inserting_new_players
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.task_group import TaskGroup

postgres_connection='cbmoron_postgres'


def trigger_evaluator(ti):
    result=ti.xcom_pull(task_ids='read_db')
    #print(result)
    print('---')
    print(result[0])
    
    if result==[]:
        print('Result == False here the exception comes')
        raise AirflowFailException('---------------NO NEW PLAYERS IN THE DATABASE---------------')
    print('New players in the database, scraping player data...')


with DAG(
    dag_id="new_player_in_database",
    schedule_interval=None,
    catchup=False,
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2022, 11, 6)
    },
) as dag:

    read_db = SQLExecuteQueryOperator(
            task_id="read_db",
            conn_id=postgres_connection,
            sql="SELECT player_id,player_link FROM players_info WHERE player_name IS NULL",
            autocommit=True,
            show_return_value_in_logs=True
        )

    should_trigger = PythonOperator(
        task_id="should_trigger",
        python_callable=trigger_evaluator
    )

    player_scraping = PythonOperator(
        task_id="scraping_new_players",
        python_callable=checking_new_players.navigating_website
    )
    with TaskGroup("inserting_to_postgres",tooltip="Task Group for inserting data into postgres DB") as inserting_data:

        inserting_players_info = PythonOperator(
            task_id="inserting_players_info",
            python_callable=inserting_new_players.inserting_players_info
        )

        inserting_player_career_path = PythonOperator(
            task_id="inserting_player_career_path",
            python_callable=inserting_new_players.inserting_players_career_path
        )

        inserting_player_stats_career = PythonOperator(
            task_id="inserting_player_stats_career",
            python_callable=inserting_new_players.inserting_players_stats_career
        )

        inserting_players_info >> inserting_player_career_path
        inserting_players_info >> inserting_player_stats_career

    read_db >> should_trigger >> player_scraping >> inserting_data