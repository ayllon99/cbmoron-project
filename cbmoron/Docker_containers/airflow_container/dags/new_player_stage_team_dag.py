from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import new_player_stage_team.inserting_new_players as inserting_new_players
import new_player_stage_team.checking_new_players as checking_new_players
import new_player_stage_team.checking_new_stages as checking_new_stages
import new_player_stage_team.checking_new_teams as checking_new_teams


url_primera=Variable.get(key='url_primera_feb')
url_segunda=Variable.get(key='url_segunda_feb')
url_tercera=Variable.get(key='url_tercera_feb')

postgres_connection='cbmoron_dev'


def trigger_evaluator_player(ti):
    result=ti.xcom_pull(task_ids='read_db_player')
    #print(result)
    print('---')
    print(result[0])
    if result==[]:
        print('Result == False here the exception comes')
        raise AirflowFailException('---------------NO NEW PLAYERS IN THE DATABASE---------------')
    print('New players in the database, scraping player data...')


def trigger_evaluator_stage(ti):
    result=ti.xcom_pull(task_ids='read_db_stages')
    #print(result)
    print('---')
    print(result[0])
    if result==[]:
        print('Result == False here the exception comes')
        raise AirflowFailException('---------------NO NEW STAGES IN THE DATABASE---------------')
    print('New stage in the database, scraping stages data...')


def trigger_evaluator_team(ti):
    result=ti.xcom_pull(task_ids='read_db_teams')
    #print(result)
    print('---')
    print(result[0])
    if result==[]:
        print('Result == False here the exception comes')
        raise AirflowFailException('---------------NO NEW TEAMS IN THE DATABASE---------------')
    print('New team in the database, scraping teams data...')


with DAG(
    dag_id="new_player_stage_team_in_database",
    schedule_interval=None,
    catchup=False,
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2022, 11, 6)
    },
) as dag:

    read_db_player = SQLExecuteQueryOperator(
            task_id="read_db_player",
            conn_id=postgres_connection,
            sql="SELECT player_id,player_link FROM players_info WHERE player_name IS NULL",
            autocommit=True,
            show_return_value_in_logs=True
        )

    should_trigger_player = PythonOperator(
        task_id="should_trigger_player",
        python_callable=trigger_evaluator_player
    )

    player_scraping = PythonOperator(
        task_id="scraping_new_players",
        python_callable=checking_new_players.navigating_website
    )

    with TaskGroup("inserting_to_postgres_player",tooltip="Task Group for inserting data into postgres DB") as inserting_data_player:

        inserting_players_info = PythonOperator(
            task_id="inserting_players_info",
            python_callable=inserting_new_players.inserting_players_info,
            op_kwargs={'postgres_connection':postgres_connection}
        )

        inserting_player_career_path = PythonOperator(
            task_id="inserting_player_career_path",
            python_callable=inserting_new_players.inserting_players_career_path,
            op_kwargs={'postgres_connection':postgres_connection}
        )

        inserting_player_stats_career = PythonOperator(
            task_id="inserting_player_stats_career",
            python_callable=inserting_new_players.inserting_players_stats_career,
            op_kwargs={'postgres_connection':postgres_connection}
        )

        inserting_players_info >> inserting_player_career_path
        inserting_players_info >> inserting_player_stats_career

    read_db_stages = SQLExecuteQueryOperator(
            task_id="read_db_stages",
            conn_id=postgres_connection,
            sql="SELECT stage_id FROM stages WHERE stage_name IS NULL",
            autocommit=True,
            show_return_value_in_logs=True
    )

    should_trigger_stage = PythonOperator(
        task_id="should_trigger_stage",
        python_callable=trigger_evaluator_stage
    )

    stage_scraping = PythonOperator(
        task_id="scraping_new_stages",
        python_callable=checking_new_stages.navigating_website,
        op_kwargs={'url_primera':url_primera,'url_segunda':url_segunda,'url_tercera':url_tercera}
    )

    inserting_stages = PythonOperator(
                task_id="inserting_stages",
                python_callable=checking_new_stages.inserting_stages,
                op_kwargs={'postgres_connection':postgres_connection}
    )


    read_db_teams = SQLExecuteQueryOperator(
            task_id="read_db_teams",
            conn_id=postgres_connection,
            sql="SELECT team_id FROM teams WHERE team_name IS NULL",
            autocommit=True,
            show_return_value_in_logs=True
    )

    should_trigger_team = PythonOperator(
        task_id="should_trigger_team",
        python_callable=trigger_evaluator_team
    )

    team_scraping = PythonOperator(
        task_id="scraping_new_teams",
        python_callable=checking_new_teams.navigating_website,
        op_kwargs={'url_primera':url_primera,'url_segunda':url_segunda,'url_tercera':url_tercera}
    )

    inserting_teams = PythonOperator(
                task_id="inserting_teams",
                python_callable=checking_new_teams.inserting_teams,
                op_kwargs={'postgres_connection':postgres_connection}
    )

    read_db_player >> should_trigger_player >> player_scraping >> inserting_data_player
    read_db_stages >> should_trigger_stage >> stage_scraping >> inserting_stages
    read_db_teams >> should_trigger_team >> team_scraping >> inserting_teams



