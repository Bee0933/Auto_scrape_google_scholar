#import libraries
import time 
import schedule
import pandas as pd 
from datetime import datetime
from selenium import webdriver

def crawl():

    #containers
    title_list = []
    links_list = []
    citation_list = []
    summary_list = []
    post_time_list = []

    # prefrences 
    base_url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0,5&q=%22Breast+cancer%22&scisbd=1'
    driver = webdriver.Firefox()
    driver.get(base_url)
    # driver.minimize_window()
    driver.maximize_window()
    time.sleep(3)

    # search data with Xpath
    for page in range(0,3):
        titles = driver.find_elements_by_xpath('//*[@class="gs_rt"]')
        links = driver.find_elements_by_xpath('//*[@class="gs_rt"]/a')
        citation = driver.find_elements_by_xpath('//*[@class="gs_a"]')
        summaries = driver.find_elements_by_xpath('//*[@class="gs_rs"]')
        post_time = driver.find_elements_by_xpath('//*[@class="gs_age"]')
        

        for i in range(len(titles)):
            title_list.append(titles[i].text.replace('[HTML]', ''))
            links_list.append(links[i].get_attribute('href'))
            citation_list.append(citation[i].text)
            summary_list.append(summaries[i].text.replace(post_time[i].text,' ').replace('...',''))
            post_time_list.append(post_time[i].text)
    
        next_pg = driver.find_element_by_link_text("Next")
        next_pg.click()
        time.sleep(3)

    # structure extracted data
    df = pd.DataFrame({'Article Title':title_list,'Article Link': links_list,'Citations':citation_list,'Summary':summary_list, 'Post Time': post_time_list })
    #save table to csv file 
    df.to_csv('crawled_data/breast_cancer.csv', index=False)
    driver.close()

if __name__ == '__main__':
    crawl()

# if __name__ == '__main__':
#     schedule.every().day.at('08:00').do(crawl) # 00:08 24 HR format which runs at local time of PC 
#     schedule.every().day.at('16:00').do(crawl)

#     while True:  
#         schedule.run_pending()
#         time.sleep(1)
