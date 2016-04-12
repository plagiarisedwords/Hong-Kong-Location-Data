import time
import math
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

#Define functions used
def PageNav_Main (EntryNum):
	#Page up / down until it is posible to access page containing entry with nav panel
	PageSource=str(driver.page_source)
	Min_NavButtons,Max_NavButtons=PageNav_GetNavOptions(PageSource)
	iteration=0
	while iteration<=10000 and not (EntryNum>=Min_NavButtons and EntryNum<=Max_NavButtons):
		if EntryNum>Max_NavButtons:
			Containstxt=str(Max_NavButtons-8)+' - '+str(Max_NavButtons+1)
			driver.find_element_by_xpath('//*[@id="_bld_result_frm:_result_tbl_paginator_bottom"]/span[4]/span[10]').click()
			WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, '_bld_result_frm:_result_tbl_paginator_bottom'), Containstxt))
			iteration+=1
		elif EntryNum<Min_NavButtons:
			Containstxt=str(Min_NavButtons+1)+' - '+str(Min_NavButtons+10)
			driver.find_element_by_xpath('//*[@id="_bld_result_frm:_result_tbl_paginator_bottom"]/span[4]/span[1]').click()
			WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, '_bld_result_frm:_result_tbl_paginator_bottom'), Containstxt))
			iteration+=1
		else:
			print('Error')
		PageSource=str(driver.page_source)
		Min_NavButtons,Max_NavButtons=PageNav_GetNavOptions(PageSource)
	
	# Determine which button should be pressed to access correct page and click that button
	Min_TableEntries,Max_TableEntries=PageNav_FindEntries(PageSource)

	if Min_TableEntries<=EntryNum and Max_TableEntries>=EntryNum:
		pass
	else:
		target_page=math.trunc(EntryNum/10)+1
		nav_target=target_page-(Min_NavButtons/10)
		Containstxt=str((target_page*10)-9)+' - '+str(target_page*10)
		target_page_xpath='//*[@id="_bld_result_frm:_result_tbl_paginator_bottom"]/span[4]/span['+str(nav_target)+']'
		driver.find_element_by_xpath(target_page_xpath).click()
		WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, '_bld_result_frm:_result_tbl_paginator_bottom'), Containstxt))

def PageNav_GetNavOptions(SourceStr):
	#Obtain entries the can be accessed on the nav panel
	NavButtons = re.findall(r'<span class="ui-paginator-page ui-state-default[a-z\-\s]*">([0-9]*)</span>',SourceStr)
	NavButtons= [int(i) for i in NavButtons]
	Min_NavButtons=(min(NavButtons)-1)*10
	Max_NavButtons=(max(NavButtons)*10)-1
	return (Min_NavButtons,Max_NavButtons)

def PageNav_FindEntries(SourceStr):
	#Obtain entries currently on the page
	TableEntries = re.findall(r'id="_bld_result_frm:_result_tbl:([0-9]*):j_id_4k',SourceStr)
	TableEntries= [int(i) for i in TableEntries]
	Min_TableEntries=min(TableEntries)
	Max_TableEntries=max(TableEntries)
	return (Min_TableEntries,Max_TableEntries)

def Selenium_click(Click_ID,Wait_ID,Wait_Str):
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, Click_ID)))
	driver.find_element_by_id(Click_ID).click()
	#WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, Wait_ID), Wait_Str))

	try:
		WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, Wait_ID), Wait_Str))
	except:
		WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, Wait_ID), Wait_Str))

def AddressClick(Num):
	#Checks that the link is active and then click if it is
	id='_bld_result_frm:_result_tbl:'+str(Num)+':j_id_4k'
	try:
		Selenium_click(id,'_detail_form:j_id_2s','Name of Building')
	except:
		Selenium_click('j_id_n:j_id_1k','_detail_form:j_id_2s','大厦名称')
		Selenium_click('j_id_n:j_id_1c','_detail_form:j_id_2s','Name of Building')
def Return_List():
	#Checks that the link is active and then click if it is
	try:
		Selenium_click('j_id_n:j_id_1c','_detail_form:j_id_2s','Name of Building')
	except:
		Selenium_click('j_id_n:j_id_1k','_detail_form:j_id_2s','大厦名称')
		Selenium_click('j_id_n:j_id_1c','_detail_form:j_id_2s','Name of Building')
	
	Selenium_click('_detail_form:j_id_3w','_bld_result_frm:pnlBldSearchResult_header','Building Search Result')

def DB_Insert(add_matrix,build_list):
	c.executemany('INSERT INTO Address VALUES (?,?,?,?)',add_matrix)
	conn.commit()
	c.execute('INSERT INTO Building VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',build_list)
	conn.commit()
	
def Scrape_Entry(Num):
	#Scrape entry in all three languages
        
	Details =[]
	Details.append(Num)
	Details .extend(re.findall(r'<div class="text">([^\n]*)\n',str(driver.page_source))[:3])
	Address1 = re.findall(r'<td role="gridcell">([^<]*)</td>',str(driver.page_source))[:5]

	try:
		Selenium_click('j_id_n:j_id_1g','_detail_form:j_id_2s','大廈名稱')
	except:
		Selenium_click('j_id_n:j_id_1c','_detail_form:j_id_2s','Name of Building')
		Selenium_click('j_id_n:j_id_1g','_detail_form:j_id_2s','大廈名稱')

	Details.extend(re.findall(r'<div class="text">([^\n]*)\n',str(driver.page_source))[:3])
	Address2=re.findall(r'<td role="gridcell">([^<]*)</td>',str(driver.page_source))[:5]

	try:
		Selenium_click('j_id_n:j_id_1k','_detail_form:j_id_2s','大厦名称')
	except:
		Selenium_click('j_id_n:j_id_1c','_detail_form:j_id_2s','Name of Building')
		Selenium_click('j_id_n:j_id_1k','_detail_form:j_id_2s','大厦名称')
	
	Details.extend(re.findall(r'<div class="text">([^\n]*)\n',str(driver.page_source))[:7])
	Address3=re.findall(r'<td role="gridcell">([^<]*)</td>',str(driver.page_source))[:5]

	counter=[]
	for x in Address1:
		counter.append(Num)
	add_matrix=list(zip(counter,Address1,Address2,Address3))
	DB_Insert(add_matrix,Details)


def Scrape_Main (Start, End):
	counter=Start
	while counter>=Start and counter<=End:
		PageNav_Main (counter)
		try:
			AddressClick(counter)
			Scrape_Entry(counter)
		except:
			print('Missed: '+str(counter))
		try:
			Return_List()
		except:
			print('Ret Failed: '+str(counter))
		counter+=1

def Scrape_Main_Single (counter):
	PageNav_Main (counter)
	try:
		AddressClick(counter)
		Scrape_Entry(counter)
	except:
		print('Missed: '+str(counter))
	try:
		Return_List()
	except:
		print('Ret Failed: '+str(counter))

#Load Firefox driver and go to the web database
driver = webdriver.Firefox()
driver.implicitly_wait(10)

#Connect to local SQLite DB
path='BuildingsDB.db'
conn=sqlite3.connect(path)
c=conn.cursor()

#Go to website
driver.get('https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true')
WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, '_bld_result_frm:pnlBldSearchResult_header'), 'Building Search Result'))	

#Scrape loop
Scrape_Main (34802,44000)


#Close connection
c.close()
conn.close()


