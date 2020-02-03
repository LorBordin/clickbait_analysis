import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from datetime import date

URL = 'https://www.dailymail.co.uk/news/index.html'
today = date.today()
path = '/Users/lorenzo/machine_learning/clickbait/webpage_scraping/archive/'
filename = 'dailymail_'+today.strftime('%d-%m-%Y')+'.cvs'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
news_container = soup.find(id="page-container")   # Contains all the news
all_articles = news_container.find_all('div', class_='article')
news_titles = []
for news in all_articles:
    title = news.find('h2', class_='linkro-darkred')
    news_titles.append(title.text.strip())
news_titles_ser = Series(news_titles)
news_titles_ser.to_csv(path+filename, header='Titles')
print('Titles saved in', path+filename+'.')


