from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import json
from datetime import datetime,timedelta

#from selenium import webdriver
#driver=webdriver.Chrome()


#url="https://baloncestoenvivo.feb.es/resultados/segundafeb/2/2024"


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


def check_new_stages(dates_left,url):
    driver=open_browser()
    
    driver.get(url)
    time.sleep(3)
    try:
        actual_stages=dates_left.keys()
    except:
        actual_stages=[]
    new_stages=bs(driver.page_source,'lxml').find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:gruposDropDownList'}).find_all('option')
    new_stages_ids=[]
    for new_stage in new_stages:
        new_stages_ids.append(new_stage.get('value'))
    new_detected=[stage_id for stage_id in new_stages_ids if stage_id not in actual_stages]
    detected=True if len(new_detected)>0 else False
    driver.quit()
    return detected,new_detected



def new_results(ti,**op_kwargs):
    url=op_kwargs['url']
    file_path=op_kwargs['file_path']
    #file_path='my_airflow_pipeline/airflow_folder/dags/segunda_feb/dates_segunda.txt'
    with open(file_path,'r') as file:
        a=file.read()
        a=a.replace("'",'"')
        if a!='':
            dates_left=json.loads(a)
        else:
            dates_left={}

    detected,new_detected=check_new_stages(dates_left,url)
    if detected:
        ti.xcom_push(key='trigger_evaluator_segunda',value=True)
        print('NEW STAGE to scrape found!')
        return True

    dates_to_scrape_dict={}
    for stage_id in dates_left.keys():
        #print(type(group))
        dates_to_scrape=[]
        for matchday,value in dates_left[stage_id].items():
            today=datetime.today()
            j=datetime.strptime(dates_left[stage_id][matchday], '%d/%m/%Y')
            if j+timedelta(3)<today:
                dates_to_scrape.append(j.strftime('%d/%m/%Y'))
        dates_to_scrape_dict[stage_id]=dates_to_scrape
        
    
    if len([value for key, sublist in dates_to_scrape_dict.items() for value in sublist])>1:
        driver=open_browser()
        time.sleep(1)
        
        driver.get(url)
        time.sleep(2.5)
        stages=bs(driver.page_source,'lxml').find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:gruposDropDownList'}).find_all('option')
        
        stages_ids=[]
        for stage in stages:
            stages_ids.append(stage.get('value'))

        for stage_id in stages_ids:
            driver.find_element(By.CSS_SELECTOR, f"option[value='{stage_id}']").click()
            time.sleep(3)
            matchdays=bs(driver.page_source,'lxml').find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')

            for match_day in range(1,len(matchdays)+1):
                matchday=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div[3]/select[3]/option[{match_day}]').text
                matchday=matchday.replace(')','')
                date=matchday.split('(')[1]
                if date in [value for key, sublist in dates_to_scrape_dict.items() for value in sublist]:
                    result=check_page(driver,match_day)
                    if result:
                        print('Date to scrape found!')
                        ti.xcom_push(key='trigger_evaluator',value=True)
                        driver.quit()
                        return True

        driver.quit()
        ti.xcom_push(key='trigger_evaluator',value=False)
        return False
            





