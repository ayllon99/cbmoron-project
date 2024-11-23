import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import os
from scraping_phase.pipeline import PostgreSQLConnection,DataPipeline


brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path
driver = webdriver.Chrome(options=options)

load_dotenv()
conn = PostgreSQLConnection(os.getenv('PG_HOST'), os.getenv('PG_DATABASE_NAME'), os.getenv('PG_USER_NAME'), os.getenv('PG_DATABASE_PASSWORD'))
conn.connect()

foreigns_df=pd.read_pickle('foreigns_df.pkl')
for a in range(len(foreigns_df)):
    url=f'https://baloncestoenvivo.feb.es/equipo/{foreigns_df.loc[a].links}'

    driver.get(url)
    time.sleep(2.5)
    soup=bs(driver.page_source)
    team_id=int(foreigns_df.loc[a].links)
    try:
        team_name=soup.find('div',{'class':'tituloSeccion'}).find('div',{'class':'wrapper-text'}).find('span',{'class':'titulo'}).text
    except:
        team_name='Nan'
    data=pd.DataFrame({'team_id':[team_id],'team_name':[team_name]})

    stats_pipeline=DataPipeline(conn,'teams')
    stats_pipeline.insert_data(data)



