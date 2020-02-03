import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from datetime import date

URL = 'https://www.telegraph.co.uk/'
today = date.today()
path = '/Users/lorenzo/machine_learning/clickbait/webpage_scraping/archive/'
filename = 'the_telegraph_'+today.strftime('%d-%m-%Y')+'.cvs'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
container = soup.find('main')
articles = container.find_all('article')
titles = [article.find('h3', class_="list-headline").text.strip() for article in articles]
titles_ser = Series(titles)
titles_ser.to_csv(path+filename, header='Titles')
print('Titles saved in', path+filename+'.')
