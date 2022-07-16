from .scrape import *
from . import scrape
from .serializers import NewsSerializer
from .models import News

def scrape():
    news_list = []
    print('- Start scraping local news.')
    news_list.extend(get_thestars())
    news_list.extend(get_malaysiastock())
    news_list.extend(get_intraday())

    total_add = 0
    total_scraped = len(news_list)
    for news in news_list:
        if News.objects.filter(headline=news['headline']).exists():
            continue
        serializer = NewsSerializer(data=news)
        if serializer.is_valid():
            serializer.save()
            total_add+=1
    
    print(f'- Web scraping process for local news done. {total_add} news from {total_scraped} scraped are added to database.')

    news_list.clear()
    print('- Start scraping international news.')
    news_list.extend(get_aljazeera())
    news_list.extend(get_investing())
    news_list.extend(get_bloomberg())

    total_add = 0
    total_scraped = len(news_list)
    for news in news_list:
        if News.objects.filter(headline=news['headline']).exists():
            continue
        serializer = NewsSerializer(data=news)
        if serializer.is_valid():
            serializer.save()
            total_add+=1
    
    print(f'- Web scraping process for international news done. {total_add} news from {total_scraped} scraped are added to database.')

    news_list.clear()
    print('- Start scraping market ideas.')
    news_list.extend(get_tradingview())

    total_add = 0
    total_scraped = len(news_list)
    for news in news_list:
        if News.objects.filter(headline=news['headline']).exists():
            continue
        serializer = NewsSerializer(data=news)
        if serializer.is_valid():
            serializer.save()
            total_add+=1
    
    print(f'- Web scraping process for market ideas done. {total_add} news from {total_scraped} scraped are added to database.')