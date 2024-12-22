import requests
from minio import Minio
from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import io


load_dotenv()


host='postgres_container'
conn=psycopg2.connect(
            dbname='cbmoron_database',
            host=host,
            user='root',
            password='root'
        )
cursor=conn.cursor()
cursor.execute("""
            SELECT player_id,player_name
            FROM players_info
                         """)


######################################################################################

driver = webdriver.Chrome()

player_id=204712
url=f'https://baloncestoenvivo.feb.es/jugador/922997/{player_id}'
driver.get(url)
#photo=driver.find_element(By.XPATH,'/html/body/form/div[4]/div[2]/div[1]/div[1]/img').screenshot_as_png
foto_link=f'https://imagenes.feb.es/Foto.aspx?c={player_id}'
for req in driver.requests:
    if req.url == foto_link:
        image_response=req.response.body
        content_length=int(req.response.headers.get('Content-Length'))
        break


"""df = pd.DataFrame(cursor.fetchall())
df.columns=['player_id','player_name']
cursor.close()
conn.close()"""

api_key=os.getenv('api_key')
pass_key=os.getenv('pass_key')
client = Minio(endpoint="localhost:9000",access_key=api_key,secret_key=pass_key,secure=False)
bucket_name = "player-image"

for player_id in df['player_id'].to_list()[:8]:
    object_name = f"{player_id}.png"
    file = io.BytesIO(image_response)
    client.put_object(bucket_name, object_name, data=file, length=content_length)

