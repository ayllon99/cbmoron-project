import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


# Open browser
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path
driver = webdriver.Chrome(options=options)
time.sleep(5)


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

        home_team_names=[]
        away_team_names=[]

        matchday=int(soup.find('h1',{'class':'titulo-modulo'}).text.strip().replace('Resultados Jornada ','')[:-12])
        trs=soup.find_all('div',{'class':'responsive-scroll'})[0].find('tbody').find_all('tr')[1:]
        for tr in trs:
                try:
                        tds=tr.find_all('td')
                        home_team_name=tds[0].find_all('a')[0].text.strip()
                        home_team_id=int(tds[0].find_all('a')[0].get('href').replace('https://baloncestoenvivo.feb.es/Equipo.aspx?i=',''))
                        away_team_name=tds[0].find_all('a')[1].text.strip()
                        away_team_id=int(tds[0].find_all('a')[1].get('href').replace('https://baloncestoenvivo.feb.es/Equipo.aspx?i=',''))
                        try:
                                home_score=int(tds[1].text.strip().split('-')[0])
                        except:
                                home_score='Nan'
                        try:
                                away_score=int(tds[1].text.strip().split('-')[1])
                        except:
                                away_score='Nan'
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
                        category=category
                        
                        match_ids.append(match_id)
                        home_team_ids.append(home_team_id)
                        away_team_ids.append(away_team_id)
                        home_team_names.append(home_team_name)
                        away_team_names.append(away_team_name)
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
        home_team_ids.extend(away_team_ids)
        home_team_names.extend(away_team_names)
        teams_df=pd.DataFrame({'team_id':home_team_ids,'team_name':home_team_names})
        return df,teams_df


#Results from 1996
url_oro='https://baloncestoenvivo.feb.es/resultados/ligaleboro/1/2023'
url_plata='https://baloncestoenvivo.feb.es/resultados/ligalebplata/2/2023'
url_eba='https://baloncestoenvivo.feb.es/resultados/ligaeba/3/2023'
category='EBA' #change with every url


results=pd.DataFrame({'match_id':[],'home_team_id':[],'away_team_id':[],'stage_id':[],'matchday':[],'home_score':[],'away_score':[],'date':[],'time':[],'match_link':[],'category':[]})
stages=pd.DataFrame({'stage_id':[],'stage_name':[],'year':[]})
teams=pd.DataFrame({'team_id':[],'team_name':[]})

driver.get(url_eba) #repeat with every url
time.sleep(5)

soup=bs(driver.page_source)
years_id=[a.get('value') for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:temporadasDropDownList'}).find_all('option')]
n_years=list(range(1,len(years_id)+1))

for n_year in n_years:
        season=years_id[n_year-1]
        next_year=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div/select[1]/option[{n_year}]')
        next_year.click()

        time.sleep(3)
        
        soup=bs(driver.page_source)
        stages_values=[a.get('value') for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:gruposDropDownList'}).find_all('option')]
        stages_names=[a.text for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:gruposDropDownList'}).find_all('option')]
        years=[season]*len(stages_names)
        stage_df=pd.DataFrame({'stage_id':stages_values,'stage_name':stages_names,'year':years})
        stages=pd.concat([stages,stage_df],axis=0).reset_index(drop=True)

        for stage in range(len(stages_names)):
                stage_name=stages_names[stage]
                stage_id=stages_values[stage]

                next_stage=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div/select[2]/option[{stage+1}]')
                next_stage.click()

                time.sleep(3)
                
                soup=bs(driver.page_source)
                matchday_ids=[a.get('value') for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')]
                matchday_name=[a.text for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')]
                
                for matchday in range(len(matchday_ids)):
                        next_matchday=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div/select[3]/option[{matchday+1}]')
                        next_matchday.click()

                        time.sleep(2)

                        soup=bs(driver.page_source)
                        df,team_ids,team_names=matchday_scraper(soup,stage_id,category)
                        team_df=pd.DataFrame({'team_id':team_ids,'team_name':team_names})
                        results=pd.concat([results,df],axis=0).reset_index(drop=True)
                        teams=pd.concat([teams,team_df],axis=0).reset_index(drop=True)

#Transforming data types and removing duplicates

results=results[results['home_score']!='Nan']
results.info()
results['match_id']=results['match_id'].astype(int)
results['home_team_id']=results['home_team_id'].astype(int)
results['away_team_id']=results['away_team_id'].astype(int)
results['stage_id']=results['stage_id'].astype(int)
results['matchday']=results['matchday'].astype(int)
results['home_score']=results['home_score'].astype(int)
results['away_score']=results['away_score'].astype(int)
results.reset_index(drop=True,inplace=True)


teams.info()
teams.drop_duplicates(inplace=True)
teams['team_id']=teams['team_id'].astype(int)
teams.reset_index(drop=True,inplace=True)

stages.info()
stages.drop_duplicates(inplace=True)
stages['stage_id']=stages['stage_id'].astype(int)
stages['year']=stages['year'].astype(int)
stages.reset_index(drop=True,inplace=True)

teams.to_pickle('teams_eba.pkl')
stages.to_pickle('stages_eba.pkl')
results.to_pickle('results_eba.pkl')