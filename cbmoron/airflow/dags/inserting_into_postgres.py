from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


def getting_sql_query(ti,table,match_id):
    df=ti.xcom_pull(task_ids='scraping_info',key=f'{match_id}_{table}')
    columns_sql = ', '.join([f'"{col}"' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    value_lists = [tuple(row) for row in df.values]
    query = f"""
        INSERT INTO {table} ({columns_sql}) 
        VALUES {', '.join(['(' + placeholders + ')' for _ in range(len(value_lists))])
    }"""
    return query, [item for sublist in value_lists for item in sublist]


def teams_match_stats_insert_data(ti):
    
    match_ids=ti.xcom_pull(task_ids='scraping_info',key='match_ids') 
    for match_id in match_ids:
        query, params=getting_sql_query(ti,'teams_matches_stats',match_id)
        print(query, params)
        SQLExecuteQueryOperator(
            task_id="upload_to_postgres",
            conn_id="cbmoron_postgres",
            sql=query,
            parameters=params,
            autocommit=True,
        ).execute(params)


def match_partials_insert_data(ti):
    match_ids=ti.xcom_pull(task_ids='scraping_info',key='match_ids') 
    for match_id in match_ids:
        query, params=getting_sql_query(ti,'match_partials',match_id)
        print(query, params)
        SQLExecuteQueryOperator(
            task_id="upload_to_postgres",
            conn_id="cbmoron_postgres",
            sql=query,
            parameters=params,
            autocommit=True,
        ).execute(params)


def players_matches_stats_insert_data(ti):
    match_ids=ti.xcom_pull(task_ids='scraping_info',key='match_ids') 
    for match_id in match_ids:
        query, params=getting_sql_query(ti,'players_matches_stats',match_id)
        print(query, params)
        SQLExecuteQueryOperator(
            task_id="upload_to_postgres",
            conn_id="cbmoron_postgres",
            sql=query,
            parameters=params,
            autocommit=True,
        ).execute(params)


def shootings_insert_data(ti):
    match_ids=ti.xcom_pull(task_ids='scraping_info',key='match_ids') 
    for match_id in match_ids:
        query, params=getting_sql_query(ti,'shootings',match_id)
        print(query, params)
        SQLExecuteQueryOperator(
            task_id="upload_to_postgres",
            conn_id="cbmoron_postgres",
            sql=query,
            parameters=params,
            autocommit=True,
        ).execute(params)


def shooting_chart_availability_insert_data(ti):
    match_ids=ti.xcom_pull(task_ids='scraping_info',key='match_ids') 
    for match_id in match_ids:
        query, params=getting_sql_query(ti,'shooting_chart_availability',match_id)
        print(query, params)
        SQLExecuteQueryOperator(
            task_id="upload_to_postgres",
            conn_id="cbmoron_postgres",
            sql=query,
            parameters=params,
            autocommit=True,
            #do_xcom_push=True,
        ).execute(params)




"""def getting_sql_query(ti):
    df=ti.xcom_pull(task_ids='scraping_info',key=table)
    table='airflow_test'
    df=ti.xcom_pull(task_ids='scraping_info',key=table)
    columns_sql = ', '.join([f'"{col}"' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    value_lists = [tuple(row) for row in df.values]

    query = f""
        INSERT INTO {table} ({columns_sql}) 
        VALUES {', '.join(['(' + placeholders + ')' for _ in range(len(value_lists))])
    }""
    return query, [item for sublist in value_lists for item in sublist]

def bulk_insert_data(ti):
    query, params=getting_sql_query(ti)
    print(query, params)
    SQLExecuteQueryOperator(
        task_id="upload_to_postgres",
        conn_id="cbmoron_postgres",
        sql=query,
        parameters=params,
        autocommit=True,
        #do_xcom_push=True,
    ).execute(params)

"""