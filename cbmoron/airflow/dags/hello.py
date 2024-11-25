import pandas as pd 
def hello(ti):
    #print('hello'*a)
    
    data = {'first_column': ['John', 'Mary', 'David', 'Jane','Pepe','manolo'],
            'second_column': ['dark','dark','blonde','red','blue','purple'],
            'third_column': ['New York', 'Chicago', 'Los Angeles', 'Miami','Sevilla','moron'],
            'forth_column': [10,25, 31, 42, 28,33]}
    df = pd.DataFrame(data)
    ti.xcom_push(key='airflow_test',value=df)
    return 'dataframeeeeeee'



