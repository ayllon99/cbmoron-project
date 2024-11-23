'''matchday_ids=[a.get('value') for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')]
matchday_name=[a.text for a in soup.find('select',{'name':'_ctl0:MainContentPlaceHolderMaster:jornadasDropDownList'}).find_all('option')]
'''
'''next_match_day=driver.find_element(By.XPATH,f'/html/body/form/div[4]/div[2]/div/select[3]/option[{3+1}]')
next_match_day.click()'''
new_url='https://baloncestoenvivo.feb.es/resultados/primerafeb/1/2024'
