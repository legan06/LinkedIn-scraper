import csv
from email.contentmanager import raw_data_manager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller

import pytz
import datetime
from pathlib import Path


import glob
import os
datetime_today=datetime.datetime.now(tz=pytz.UTC)
datetime_lizbon=datetime_today.astimezone(pytz.timezone("Europe/Lisbon"))
"""""
file_path=str(Path(__file__).parent.resolve().parent.parent)+r"\1-target-urls"
name_of_output = f"\BDG-BPIEX-{datetime_lizbon.strftime('%y')}{datetime_lizbon.strftime('%m')}-target-urls.csv"  
print(str(file_path))
"""""
chromedriver_autoinstaller.install()

#PROXY="88.247.138.7:56387"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1280,800")
#chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--headless")
chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36.')  
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
driver=webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.linkedin.com/")

           



with open("User_Pass.txt","r")as file:
    all_lines=file.readlines()

username=""
password=""
if all_lines!=[]:
    username=all_lines[0].replace("\n","")
    password=all_lines[1].replace("\n","")

def login():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//input[@autocomplete="username"]'))).send_keys(username)
    driver.find_element_by_xpath('//input[@autocomplete="current-password"]').send_keys(password)
    
def search(url_list):
    post_url=[]
    post_caption=[]
    post_date=[]
    for url in url_list:
        driver.get(url)    
        try:
            post_url.append(WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='app-aware-link feed-mini-update-optional-navigation-context-wrapper']")))[0].get_attribute('href'))
            post_capt=WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="display-flex flex-row"]/a')))[0].get_attribute('aria-label').replace("View full post. ","")
            if post_capt=="Image":
                post_capt=WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="display-flex flex-row"]/a')))[1].get_attribute('aria-label').replace("View full post. ","")
            post_caption.append(post_capt)
        except:
            post_url.append("")
            post_caption.append("")
            pass
        try:
            post_date.append(WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="feed-mini-update-contextual-description__text"]/span')))[0].text.split("•")[1].strip())
        except:
            post_date.append("")
            pass
    combine_list=zip(url_list,post_url,post_caption,post_date)
    return combine_list

def read():
    url_list=[]
    for filename in glob.glob('*.csv'):
        with open(filename, 'r') as f:
            for a in f.readlines():
                url_list.append(a.replace("ï»¿","").replace("\n",""))


    return url_list

login()

while True:
    if "linkedin.com/feed" in driver.current_url:
        url_list=read()
        print(url_list)
        combine_list= search(url_list)
        with open("output_File.csv","a+", encoding="utf8", newline='') as file:
            wr=csv.writer(file)
            wr.writerow(("Url", "Post_Url","Caption","Date"))
            for row in combine_list:
                wr.writerow(row)

                
        break    
        
