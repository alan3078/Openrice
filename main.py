# Import Libraries

from bs4 import BeautifulSoup
import requests
import re
import os
import warnings
import pandas as pd

warnings.filterwarnings("ignore")

def scrape_rstr(id):
    
    # Accessing Menu Page
    URL = 'https://www.openrice.com/zh/hongkong/menu/'+str(id)+'/takeaway?source=poiDetail'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    r = requests.get(URL,headers=headers)
    
    # Finding Main Page from bs
    soup = BeautifulSoup(r.content,'html.parser')
    if r.status_code==200:
        try:
            # if it's not an empty page
            sub_url = soup.find_all('a',text='概要')[0].attrs['href']
            full_url = 'https://www.openrice.com' + sub_url
            r = requests.get(full_url,headers=headers)
            soup = BeautifulSoup(r.content,'html.parser')
            
            # Logging the entire html page
            with open("'C:/Development/OpenriceScraper/src/data/"+str(id)+".txt","w") as f:
                f.write(r.text)
            rstr_name = soup.find("span",class_='name').text
            return rstr_name+' logged'
        except:
            # if it's an empty page
            return 'Empty page'
    else:
        return 'Non-existent' 

def scrape_range(from_,to_):
    # Get list of searched ID
    with open('C:/Development/OpenriceScraper/src/data/result.txt','r') as searched_log:
        searched = [int(id) for id in searched_log.readlines()]
        
    # Start scraping   
    for i in range(from_,to_):
        if i<100000:
            i = str(i).zfill(6)
        with open('C:/Development/OpenriceScraper/src/data/result.txt','a') as searched_log:
            if i not in searched:
                status = scrape_rstr(i)
                if status!='Non-existent':
                    print(f"{i}: {status}")
                searched_log.write(str(i)+'\n')
                
scrape_range(0,100000)