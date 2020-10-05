import requests
from bs4 import BeautifulSoup
import articles
from datetime import datetime
import os

DAYS_INTERVAL=7
ARTICLE_TEMPLATE='''
<article> 
    <header>{header}</header>
    <p class="annotation">{annotation}</p>
    <figure> <img src="{imgEncoded}"> </figure>
    <section>{text}</section>
    <footer>{source}, {date:%d.%m.%Y}</footer>
</article>
'''
def xakepDateFunc(article, soup):
    article.date=articles.getDateFromString(article.url)

settings = articles.Settings(
    headerSelector="h1.post-title", 
    sourceName="xakep.ru", 
    annotationSelector="article.post p", 
    imageSelector="a.bdaia-featured-img-cover",
    textSelector="article.post", 
    removeSelector="script, style, meta, form, button, footer, div#current_issue_box", 
    dateCallback=xakepDateFunc)
filename = '''news_{date:%Y%m%d_%H%M}.html'''.format(date=datetime.today())
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
req = requests.get("https://xakep.ru/")
soup = BeautifulSoup(req.text, "lxml")
links = soup.select('.bd-main .entry-title > a')
print('Number of article links:', len(links))
text_file = open(filename, "a", encoding='utf-8')
for link in links:
    print("Start parsing ", link["href"])
    article = articles.Article(link["href"], settings)
    html = article.toString(ARTICLE_TEMPLATE)
    print("SUCCESSFULLY PARSED: \t", link["href"])
    if((datetime.today()-article.date).days > DAYS_INTERVAL):
        print("This article is OLD")
        break
    text_file.write(html)
text_file.close()
