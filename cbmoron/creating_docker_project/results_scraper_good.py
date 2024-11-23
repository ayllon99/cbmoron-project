import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from datetime import datetime


def matchday_scraper(soup,stage_id,category):
        match_ids=[]
        home_team_ids=[]
        away_team_ids=[]
        stage_ids=[]
        matchdays=[]
        home_scores=[]
        away_scores=[]
        dates=[]
        times=[]
        match_links=[]
        categories=[]

        matchday=int(soup.find('h1',{'class':'titulo-modulo'}).text.strip().replace('Resultados Jornada ','')[:-12])
        trs=soup.find_all('div',{'class':'responsive-scroll'})[0].find('tbody').find_all('tr')[1:]
        for tr in trs:
                try:
                        tds=tr.find_all('td')
                        home_team_id=int(tds[0].find_all('a')[0].get('href').replace('https://baloncestoenvivo.feb.es/Equipo.aspx?i=',''))
                        away_team_id=int(tds[0].find_all('a')[1].get('href').replace('https://baloncestoenvivo.feb.es/Equipo.aspx?i=',''))
                        
                        home_score=int(tds[1].text.strip().split('-')[0])
                        away_score=int(tds[1].text.strip().split('-')[1])
                
                        match_link=tds[1].find('a').get('href')
                        match_id=int(match_link.replace('https://baloncestoenvivo.feb.es/Partido.aspx?p=',''))
                        try:
                                date=datetime.strptime(tds[2].text.strip(),'%d/%m/%Y').date()
                        except:
                                date=datetime.strptime('01/01/1900','%d/%m/%Y').date()
                        try:
                                time=datetime.strptime(tds[3].text.strip(),'%H:%M').time()
                        except:
                                time=datetime.strptime('00:00','%H:%M').time()
                    
                        match_ids.append(match_id)
                        home_team_ids.append(home_team_id)
                        away_team_ids.append(away_team_id)
                        stage_ids.append(stage_id)
                        matchdays.append(matchday)
                        home_scores.append(home_score)
                        away_scores.append(away_score)
                        dates.append(date)
                        times.append(time)
                        match_links.append(match_link)
                        categories.append(category)
                except:
                        print(f'Error in {tr}')

        df=pd.DataFrame({'match_id':match_ids,'home_team_id':home_team_ids,'away_team_id':away_team_ids,'stage_id':stage_ids,'matchday':matchdays,'home_score':home_scores,'away_score':away_scores,'date':dates,'time':times,'match_link':match_links,'category':categories})
        
        return df


#this is temp and should be in navigating.py
#I just receive the driver class already active
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path
driver = webdriver.Chrome(options=options)
time.sleep(5)

#temporal, this should go in navigating.py
new_url='https://baloncestoenvivo.feb.es/resultados/primerafeb/1/2024'

driver.get(new_url)

soup=bs(driver.page_source)

results=matchday_scraper(soup,stage_id=86340,category='primera_feb')













































