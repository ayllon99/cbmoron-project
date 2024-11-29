from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import json
from datetime import datetime,timedelta
import os
from airflow.models import Variable


url=Variable.get(key='url_tercera_feb')


def check_page(driver,match_day):
    driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div[3]/select[3]/option[{match_day}]').click()
    time.sleep(2.5)
    soup=bs(driver.page_source,'lxml')
    trs=soup.find_all('div',{'class':'responsive-scroll'})[0].find('tbody').find_all('tr')[1:]
    n_matches=[]
    for tr in trs:
        try:
            tds=tr.find_all('td')
            home_score=int(tds[1].text.strip().split('-')[0])
            away_score=int(tds[1].text.strip().split('-')[1])
            match_link=tds[1].find('a').get('href')
            n_matches.append(match_link)
        except:
            pass
    if len(n_matches)==len(trs):
        return True
    else:
        return False


def open_browser():
    sw_options = {
            'addr': '0.0.0.0',  # Address of the machine running Selenium Wire. Explicitly use 127.0.0.1 rather than localhost if remote session is running locally.
            'auto_config': False,
            'port': 35813
            }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=airflow-container:35813')
    chrome_options.add_argument('--ignore-certificate-errors')


    driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444",
        options=chrome_options,
        seleniumwire_options=sw_options
        )
    return driver


def new_results(ti):

    print(os.path.join(os.path.dirname(__file__), 'tercera_feb/dates_tercera.txt'))
    file_path = os.path.join(os.path.dirname(__file__), 'tercera_feb/dates_tercera.txt')
    #file_path='my_airflow_pipeline/airflow_folder/dags/tercera_feb/dates_tercera.txt'
    with open(file_path,'r') as file:
        a=file.read()
        a=a.replace("'",'"')
        dates_left=json.loads(a)

    
    dates_to_scrape_dict={}
    for group in dates_left.keys():
        #print(type(group))
        dates_to_scrape=[]
        for matchday,value in dates_left[group].items():
            today=datetime.today()
            j=datetime.strptime(dates_left[group][matchday], '%d/%m/%Y')
            if j+timedelta(3)<today:
                dates_to_scrape.append(j.strftime('%d/%m/%Y'))
        dates_to_scrape_dict[group]=dates_to_scrape
        
    
    
    matches_ready={}
    matches_to_delete={}
    if len([value for key, sublist in dates_to_scrape_dict.items() for value in sublist])>1:
        driver=open_browser()
        time.sleep(1)
        driver.get(url)
        time.sleep(2.5)
        matchdays_list=bs(driver.page_source,'lxml').find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')
        groups_list=bs(driver.page_source,'lxml').find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:gruposDropDownList'}).find_all('option')

        for group in range(1,len(groups_list)+1):
            driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div[3]/select[2]/option[{group}]').click()
            time.sleep(3)
            dates_to_delete=[]
            match_days=[]
            for match_day in range(1,len(matchdays_list)+1):
                matchday=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div[3]/select[3]/option[{match_day}]').text
                matchday=matchday.replace(')','')
                date=matchday.split('(')[1]
                if date in [value for key, sublist in dates_to_scrape_dict.items() for value in sublist]:
                    result=check_page(driver,match_day)
                    if result:
                        dates_to_delete.append(date)
                        match_days.append(match_day)
            matches_ready[group]=match_days
            matches_to_delete[group]=dates_to_delete


        new_dict = {}
        for key, jornadas in dates_left.items():
            if key in matches_to_delete:
                new_dict[key] = {jornada: date for jornada, date in jornadas.items() if date not in matches_to_delete[key]}
            else:
                new_dict[key] = jornadas


        with open(file_path,'w') as file:
            json.dump(new_dict,file)

        driver.quit()

        if len([value for key,sublist in matches_ready.items()for value in sublist])>0:
            groups=[]
            for group in range(len(groups_list)):
                ti.xcom_push(key=f'{group}_match_days',value=matches_ready[group])
                groups.append(group)
            ti.xcom_push(key=f'groups',value=groups)
            return True
        else:
            return False








