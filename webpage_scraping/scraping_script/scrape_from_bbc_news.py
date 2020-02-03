import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from datetime import date

URL = 'https://www.bbc.co.uk/news'
today = date.today()
path = '/Users/lorenzo/machine_learning/clickbait/webpage_scraping/archive/'
filename = 'bbc_news_'+today.strftime('%d-%m-%Y')+'.cvs'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
container = soup.find(id="latest-stories-tab-container")
articles = container.find_all('h3', class_="gs-c-promo-heading__title")
titles = [article.text for article in articles]

unique_titles = []
unique_titles.append(titles[0])

# Remove duplicates -- not unsed np.unique to maintain the original order
for title in titles:
    counter = 0
    for unique_title in unique_titles:
        if title == unique_title:
            counter += 1
    if counter == 0:
        unique_titles.append(title)
        
title_ser = Series(unique_titles)
title_ser.to_csv(path+filename, header='Titles')
print('Titles saved in', path+filename+'.')
