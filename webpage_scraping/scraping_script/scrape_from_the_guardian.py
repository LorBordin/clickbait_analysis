import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from datetime import date

# Functions

def take_title(container):
    head = container.find('div', class_="fc-container__header__title")
    if  head is not None:
        head = head.text.strip()
        if 'Headlines' in head.split():
            head = 'Headlines'
        return head
    else:
        return 'No head'

def collect_news(container):
    news = container.find_all(class_="u-faux-block-link__overlay js-headline-text")
    news_titles = [article.text.strip() for article in news]
    return news_titles
    

def scrape_titles_from_Guardian(soup):
    
    containers = soup.find_all('div', class_='fc-container__inner')
    interesting_sections = ['Headlines','Spotlight','Opinion','Sport','From the UK','Around the world','Culture',
                            'Lifestyle','Explore','In pictures','Most viewed']
    articles_dict = {}
    for container in containers:
        head = take_title(container)
        if head in interesting_sections:
            news_titles = collect_news(container)
            articles_dict[head] = news_titles
    return articles_dict

# Main Body

URL = 'https://www.theguardian.com/uk'

today = date.today()
path = '/Users/lorenzo/machine_learning/clickbait/webpage_scraping/archive/'
filename = 'the_guardian_'+today.strftime('%d-%m-%Y')+'.cvs'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
containers = soup.find_all('div', class_='fc-container__inner')
today_titles = scrape_titles_from_Guardian(soup)
today_titles_df = DataFrame(dict([(k,Series(v)) for k,v in today_titles.items()]))
today_titles_df.to_csv(path+filename)
print('Titles saved in', path+filename+'.')

