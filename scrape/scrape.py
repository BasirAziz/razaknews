import time
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime as dt
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytz import timezone

def get_thestars():
    print('- Scraping https://www.thestar.com.my')
    news_list = []
    try:
        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        driver.get('https://www.thestar.com.my/tag/corporate+news')
        element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.ID,'loadMorestories' ))
            )
        element.click()
        time.sleep(2)
        page = driver.page_source
        page_soup = BeautifulSoup(page, 'html.parser')

        for section in page_soup.find_all('div',attrs={'class':'row list-listing'}):
            header=section.find('a')
            time_str=section.find('label',attrs={'class':'timestamp'}).text
            news_datetime=dt.datetime.strptime(time_str,r'%d %b %Y | %I:%M %p')
            new_news = {
                    'headline' : header.text,
                    'url' : 'https://www.thestar.com.my'+header.get('href'),
                    'source' : 'thestar.com.my',
                    'type' : 0,
                    'timestamp' :  news_datetime
                }
            news_list.append(new_news)
        driver.quit()
        print('- Scrape https://www.thestar.com.my done')
    except:
        print('- Scraping from https://www.thestar.com.my failed')
    finally:
        return news_list

def get_malaysiastock():
    print('- Scraping https://www.malaysiastock.biz')
    news_list = []
    try:
        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        driver.get('https://www.malaysiastock.biz/Blog/Blog-Headlines.aspx')
        page = driver.page_source
        page_soup = BeautifulSoup(page, 'html.parser')

        date_text = ''
        for tr_tag in page_soup.select('#MainContent_tbNews > tbody > tr'):
            new_news=''
            if tr_tag.find('span', attrs={'class':'blogTitle'}) is not None:
                date_text=tr_tag.find('span', attrs={'class':'blogTitle'}).text
            if tr_tag.find('table', attrs={'class':'tbNewsList'}) is not None:
                news=tr_tag.find('table', attrs={'class':'tbNewsList'})
                time_text = news.find('td').text
                news_datetime=dt.datetime.strptime((date_text+' '+time_text),r'%a, %d %b %Y %I:%M %p')
                header=news.find('a', attrs={'rel':'nofollow'})
                new_news = {
                    'headline' : header.text,
                    'url' : header.get('href'),
                    'source' : 'malaysiastock.biz',
                    'type' : 0,
                    'timestamp' :  news_datetime
                }
                news_list.append(new_news)
        driver.quit()
        print('- Scrape https://www.malaysiastock.biz done')
    except:
        print('- Scraping from https://www.malaysiastock.biz failed')
    finally:
        return news_list


def get_intraday():
    print('- Scraping https://www.intraday.my')
    news_list = []
    try:
        news_links= ['https://intraday.my/category/biz/','https://intraday.my/category/isu-semasa/','https://intraday.my/category/artikel-umum/']
        TIME_XPATH='/html/body/div[1]/div[3]/main/div/div/div[1]/div[1]/article/div[2]/div/div[2]/span/time/b'
        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        for link in news_links:
            driver.get(link)
            main_window = driver.window_handles[0]

            for news in driver.find_elements_by_class_name('listing-item-grid-1 '):
                html = news.get_attribute('innerHTML')
                html_soup = BeautifulSoup(html,'html.parser')
                header = html_soup.find('a',{'class':'post-title post-url'})
                new_news = {
                    'headline' : header.text.rstrip(),
                    'url' : header.get('href'),
                    'source' : 'intraday.my',
                    'type' : 0
                }
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(header.get('href'))
                element = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH, TIME_XPATH))
                )
                html = element.get_attribute('innerHTML')
                html_soup = BeautifulSoup(html,'html.parser')

                time_str = html_soup.text  
                news_datetime = dt.datetime.strptime(time_str, r'%d %b %Y %I:%M %p')
                new_news['timestamp'] = news_datetime
                news_list.append(new_news)
                driver.close()
                driver.switch_to.window(main_window)
        driver.quit()
        print('- Scrape https://www.intraday.my done')
    except:
        print('- Scraping from https://www.intraday.my failed')
    finally:
        return news_list

def get_bloomberg():
    print('- Scraping https://www.thestar.com.my')
    news_list = []
    try:
        TIME_XPATH='/html/body/main/div/article/div/div[1]/div/div/div/div[2]/time'

        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        driver.get('https://www.bloomberg.com/markets/economics')
        main_window = driver.window_handles[0]

        for news in driver.find_elements_by_class_name('story-package-module__story'):
            html = news.get_attribute('innerHTML')
            html_soup = BeautifulSoup(html,'html.parser')
            header = html_soup.find('a',{'class':'story-package-module__story__headline-link'})
            new_news = {
                    'headline' : header.text.replace('\n','').replace('                ','').replace('            ',''),
                    'url' : 'https://www.bloomberg.com'+header.get('href'),
                    'source' : 'bloomberg.com',
                    'type' : 1,
                }
            if new_news in news_list:
                continue
            element = news.find_element_by_xpath('./h3/a')
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get('https://www.bloomberg.com'+header.get('href'))
            element = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, TIME_XPATH))
            )
            html = element.get_attribute('innerHTML')
            html_soup = BeautifulSoup(html,'html.parser')

            time_str = html_soup.text
            time_splits = time_str.split()
            time_str = time_splits[0]+time_splits[1]+time_splits[2]+time_splits[3]+time_splits[4]    

            news_datetime = dt.datetime.strptime(time_str, r'%A%d,%Y %I:%M%p')
            new_news['timestamp'] = news_datetime
            news_list.append(new_news)
            driver.close()
            driver.switch_to.window(main_window)
        driver.quit()
        print('- Scrape https://www.thestar.com.my done')
    except:
        print('Scraping from https://www.bloomberg.com failed')
    finally:
        return news_list

def get_investing():
    print('- Scraping https://www.investing.com')
    news_list = []
    try:
        TIME_XPATH = '//*[@id="leftColumn"]/div[1]/span'

        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        driver.get('https://www.investing.com/news/latest-news')
        main_window = driver.window_handles[0]

        for news in driver.find_elements_by_class_name('js-article-item'):
            html = news.get_attribute('outerHTML')
            html_soup = BeautifulSoup(html, 'html.parser')
            if html_soup.find('article', attrs={'class':'sponsoredArticle'}):
                continue
            header = html_soup.find('a',{'class':'title'})
            new_news = {
                    'headline' : header.get('title'),
                    'url' : 'https://www.investing.com'+header.get('href'),
                    'source' : 'investing.com',
                    'type' : 1,
                }
            if new_news in news_list:
                continue
            element = news.find_element_by_xpath('./div[1]/a')
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get('https://www.investing.com'+header.get('href'))
            element = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, TIME_XPATH))
            )
            html = element.get_attribute('innerHTML')
            html_soup = BeautifulSoup(html,'html.parser')

            time_str = html_soup.text
            time_splits = time_str[time_str.find("(")+1:time_str.find(")")].split()
            time_str = time_splits[0]+time_splits[1]+time_splits[2]+time_splits[3]  

            et_timezone = timezone('US/Eastern')
            news_datetime = dt.datetime.strptime(time_str, r'%b%d,%Y%I:%M%p')
            news_datetime = et_timezone.localize(news_datetime)
            new_news['timestamp'] = news_datetime
            news_list.append(new_news)
            driver.close()
            driver.switch_to.window(main_window)
        driver.quit()
        print('- Scrape https://www.investing.com done')
    except:
        print('- Scraping from https://www.investing.com failed')
    finally:
        return news_list

def get_aljazeera():
    print('- Scraping https://www.aljazeera.com')
    news_list = []
    try:
        news_links= ['https://www.aljazeera.com/economy/','https://www.aljazeera.com/us-canada/']
        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        for link in news_links:
            print(link)
            driver.get(link)
            page = driver.page_source
            page_soup = BeautifulSoup(page,'html.parser')

            upper_content = page_soup.find('div',attrs={'class':'container--section-top-grid'}) 
            for article in upper_content.find_all('article',attrs={'class':'gc--type-post'}):
                header = article.find('div',attrs={'class':'gc__content'}).find('a')
                time_str = article.find('div',attrs={'class':'date-simple'}).text
                news_datetime = dt.datetime.strptime(time_str,r'%d %b %Y')
                new_news = {
                    'headline' : header.find('span').text,
                    'url' : 'https://www.aljazeera.com'+header.get('href'),
                    'source' : 'aljazeera.com',
                    'type' : 1,
                    'timestamp' :  news_datetime
                }
                if new_news in news_list:
                    continue
                news_list.append(new_news)

            bottom_content = page_soup.find('div',attrs={'class':'container__inner container--section-more-ads'}) 
            for article in bottom_content.find_all('article',attrs={'class':'gc--type-post'}):
                header = article.find('div',attrs={'class':'gc__content'}).find('a')
                time_str = article.find('div',attrs={'class':'date-simple'}).text
                news_datetime = dt.datetime.strptime(time_str,r'%d %b %Y')
                new_news = {
                    'headline' : header.find('span').text,
                    'url' : 'https://www.aljazeera.com'+header.get('href'),
                    'source' : 'aljazeera.com',
                    'type' : 1,
                    'timestamp' :  news_datetime
                }
                if new_news in news_list:
                    continue
                news_list.append(new_news)

        driver.quit()
        print('- Scrape https://www.aljazeera.com done')
    except:
        print('- Scraping from https://www.aljazeera.com failed')
    finally:
        return news_list

def get_tradingview():
    print('- Scraping https://www.tradingview.com')
    news_list = []
    try:
        news_links = ['https://my.tradingview.com/markets/stocks-malaysia/ideas/','https://www.tradingview.com/ideas/']
        options = Options()
        options.headless = True
        options.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(executable_path=r'scrape/chromedriver.exe',options=options)
        for link in news_links:
            driver.get(link)
            page = driver.page_source   
            page_soup = BeautifulSoup(page, 'html.parser')

            for article in page_soup.find_all('div',attrs={'class':'tv-feed__item js_cb_class tv-feed-layout__card-item js-feed__item--inited'}):
                header = article.find('a')
                date_element = article.find('span', attrs={'class':'tv-card-stats__time'})
                news_datetime = dt.datetime.fromtimestamp(float(date_element.get('data-timestamp')))
                new_news = {
                    'headline' : header.text,
                    'url' : 'https://www.tradingview.com'+header.get('href'),
                    'source' : 'tradingview.com',
                    'type' : 2,
                    'timestamp' : news_datetime,
                }
                if new_news in news_list:
                    continue
                news_list.append(new_news)

        driver.quit()
        print('- Scrape https://www.tradingview.comdone')
    except:
        print('- Scraping from https://www.tradingview.com failed')
    finally:
        return news_list