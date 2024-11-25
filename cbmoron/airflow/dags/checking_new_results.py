from bs4 import BeautifulSoup as bs
import time
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import json
from datetime import datetime,timedelta
import os

def check_page(driver,a):
    driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div[3]/select[3]/option[{a}]').click()
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


def new_results(ti):
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

    driver.get("https://baloncestoenvivo.feb.es/resultados/primerafeb/1/2024")
    time.sleep(2.5)
    options=bs(driver.page_source,'lxml').find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')

    #{"Jornada 1": "27/09/2024","Jornada 2": "04/10/2024", "Jornada 3": "11/10/2024", "Jornada 4": "18/10/2024", "Jornada 5": "25/10/2024", "Jornada 6": "01/11/2024", "Jornada 7": "08/11/2024", "Jornada 8": "15/11/2024", "Jornada 9": "01/12/2024", "Jornada 10": "06/12/2024", "Jornada 11": "10/12/2024", "Jornada 12": "15/12/2024", "Jornada 13": "20/12/2024", "Jornada 14": "29/12/2024", "Jornada 15": "03/01/2025", "Jornada 16": "10/01/2025", "Jornada 17": "17/01/2025", "Jornada 18": "31/01/2025", "Jornada 19": "07/02/2025", "Jornada 20": "11/02/2025", "Jornada 21": "15/02/2025", "Jornada 22": "02/03/2025", "Jornada 23": "07/03/2025", "Jornada 24": "11/03/2025", "Jornada 25": "16/03/2025", "Jornada 26": "21/03/2025", "Jornada 27": "28/03/2025", "Jornada 28": "04/04/2025", "Jornada 29": "11/04/2025", "Jornada 30": "18/04/2025", "Jornada 31": "22/04/2025", "Jornada 32": "27/04/2025", "Jornada 33": "02/05/2025", "Jornada 34": "09/05/2025"}
    print(os.path.join(os.path.dirname(__file__), 'dates.txt'))
    file_path = os.path.join(os.path.dirname(__file__), 'dates.txt')
    with open(file_path,'r') as file:
        a=file.read()
        a=a.replace("'",'"')
        dates=json.loads(a)

    dates_to_scrape=[]
    dates_to_delete=[]

    for key,value in dates.items():
        today=datetime.today()
        j=datetime.strptime(dates[key], '%d/%m/%Y')
        if j+timedelta(3)<today:
            dates_to_scrape.append(j.strftime('%d/%m/%Y'))

    aa=[]
    for a in range(1,len(options)+1):
        matchday=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div[3]/select[3]/option[{a}]').text
        matchday=matchday.replace(')','')
        date=matchday.split('(')[1]
        if date in dates_to_scrape:
            result=check_page(driver,a)
            if result:
                dates_to_delete.append(date)
                aa.append(a)

    for value in dates_to_delete:
        if value in dates.values():
            key_to_delete = [key for key, val in dates.items() if val == value][0]
            del dates[key_to_delete]

    with open(file_path,'w') as file:
        json.dump(dates,file)

    driver.quit()
    if len(aa)>0:
        ti.xcom_push(key='aa',value=aa)
        return True
    else:
        return False













