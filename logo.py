#!/usr/bin/python3
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.by import By
import urllib

chrome_driver_binary = "/Users/alonbaruch/Desktop/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary)

# 1. Get access to google sheet
# 2. Get all website urls from google sheet
# 3. Create a folder for logos
# 4. Download logo for every college

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/alonbaruch/Downloads/CC_SB-master/client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("Remaining Colleges").sheet1


# function to pull urls from gogolesheet
def getLogoURLS(driver):
	URLArr = sheet.col_values(5)
	return URLArr

def getLogoTitles(driver):
	TitleArr = sheet.col_values(2)
	return TitleArr

#lists containing video data
logo_URLS = getLogoURLS(driver)
logo_Titles = getLogoTitles(driver)

# function for getting the logo from a url and downloading image
def getLogo(driver):

	row_count = 0	

	driver.get("https://clearbit.com/logo")
	inp = driver.find_element_by_css_selector(".input input")

	for x in logo_URLS:
		keys = x

		inp.send_keys(keys)
		inp.send_keys(u'\ue007')

		time.sleep(10)

		res = driver.find_element_by_css_selector(".result img").get_attribute("src")

		college = logo_Titles[row_count]

		urllib.urlretrieve(res, "/Users/alonbaruch/Desktop/logos/"+str(college)+".png")

		row_count += 1

		inp.clear()

	
	#closes browser
	driver.close();

getLogo(driver)
