import os

path = 'scraping_script/'
prefix = 'scrape_from_'
journals = ['the_guardian', 'dailymail', 'bbc_news', 'the_telegraph']

for journal in journals:
    print('Collecting titles from '+journal+'...')
    os.system('python '+path+prefix+journal+'.py')
    print()

print('Done.')
