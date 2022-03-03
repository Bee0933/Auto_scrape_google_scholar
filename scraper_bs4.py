import pandas as pd 
import requests
import random
import math
import schedule
import time
from datetime import datetime
from bs4 import BeautifulSoup

def crawl():
        
    # multiple headers 
    user_agents = [ 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
    ]   
    # containers
    article_links = []
    name_article = []
    summary = []
    citations = []

    page_num = 0
    max = 10

    while page_num < max:
        proxy_URL = "http://api.proxiesapi.com"
        auth_key = '6dece0e3574f25ddef45db32971865a7_sr98766_ooPq87'
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent} 
        base_url = f'https://scholar.google.com/scholar?start={page_num}0&q=stoke+and+TAVR&hl=en&as_sdt=0,5'
        PARAMS = {'auth_key':auth_key, 'url':base_url} 

        response = requests.get(url = proxy_URL, params=PARAMS, headers=headers) 
        # response = requests.get(base_url, headers=headers)

        if response.status_code == 200:
            print(f'site request successful for page {page_num}')

            soup = BeautifulSoup(response.content, 'html.parser')
        
            # page_r = soup.findAll('div', {'class':'gs_ab_mdw'})
            cards = soup.findAll("div", {'class':'gs_ri'})
            page_r = soup.findAll('div', {'class':'gs_ab_mdw'})
            # page_range = page_r[1].get_text()
            # page_range = math.ceil([int(i) for i in page_range.split() if i.isdigit()][-1]/10)
            # max = page_range

            for card in cards:
                links = card.find('a', href=True)
                try:
                    summary.append(card.find('div', {'class':'gs_rs'}).get_text())
                except:
                    summary.append('n/a')
                try:
                    name_article.append(links.get_text())
                except:
                    name_article.append('n/a')
                try:  
                    article_links.append(links['href'])
                except:
                    article_links.append('n/a')
                try:
                    citations.append(card.find('div', {'class':'gs_a'}).get_text())
                except:
                    citations.append('n/a')            
        else:
            print('site request failed', f'\n error: {response.status_code}')

        time.sleep(3)
        page_num+=1
        
    data = {
        'Article Name':name_article, 'Citations':citations, 'summary':summary,'Link to Article' : article_links
    }
    dataFrame = pd.DataFrame(data=data)

    import os 
    pwd = os.getcwd()
    sav_dir = os.path.join(pwd,'crawled_data/stroke&TAVR-googleScholar.csv')
    dataFrame.to_csv(sav_dir,index=False)


if __name__ == '__main__':
    crawl()

# if __name__ == '__main__':
#     schedule.every(1).hours.do(crawl)

#     while True:  
#         schedule.run_pending()
#         time.sleep(1)

# 
