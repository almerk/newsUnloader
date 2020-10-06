import requests
from bs4 import BeautifulSoup
import articles
from datetime import datetime
import os
import settings
from urllib.parse import urljoin


filename = '''news_{date:%Y%m%d_%H%M}.html'''.format(date=datetime.today())
temp_filename = filename+".tmp"
if os.path.exists(temp_filename):
    os.remove(temp_filename)
for source in settings.SOURCES:
    for url in source['urls']:
        text_file = open(temp_filename, "a", encoding='utf-8')
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")
        links = soup.select(source['linkSelector'])
        print('Number of article links:', len(links))
        for link in links:
            href = urljoin(url, link["href"])
            print("Start parsing ", href)
            article = articles.Article(href, source["settings"])
            html = article.toString(settings.ARTICLE_TEMPLATE)
            print("SUCCESSFULLY PARSED: \t", link["href"])
            if((datetime.today()-article.date).days > settings.DAYS_INTERVAL):
                print("This article is OLD. Stopped searching on this source")
                break
            text_file.write(html)
        text_file.close()

articlesFile = open(temp_filename, encoding='utf-8')
result = settings.ResultTemplate.format(articles=articlesFile.read())
articlesFile.close()
resultFile = open(filename, "w", encoding='utf-8')
resultFile.write(result)
resultFile.close()
os.remove(temp_filename)
print("News unload saved in '%s'" % filename)
