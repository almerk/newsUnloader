import articles
from datetime import datetime

DAYS_INTERVAL=7
ARTICLE_TEMPLATE='''
<article>
    <button>Удалить статью</button>
    <header>{header}</header>
    <p class="annotation">{annotation}</p>
    <figure> <img src="{imgEncoded}"> </figure>
    <section>{text}</section>
    <footer>{source}, {date:%d.%m.%Y}</footer>
</article>'''
def xakepDateFunc(article, soup):
    article.date=articles.getDateFromString(article.url)
def securitylabDateFunc(article, soup):
    time = soup.select_one("div.article-options time")["datetime"]
    article.date=datetime.strptime(time[:10], "%Y-%m-%d")

SOURCES = [
    {'urls':['https://xakep.ru/'],
     'linkSelector': '.bd-main .entry-title > a',
     'settings': articles.Settings(
    headerSelector="h1.post-title", 
    sourceName="xakep.ru", 
    annotationSelector="article.post p", 
    imageSelector="a.bdaia-featured-img-cover",
    textSelector="article.post", 
    removeSelector="script, style, meta, form, button, footer, div#current_issue_box", 
    dateCallback=xakepDateFunc,
    textRemoveSelector=["p"])},
    {'urls':['https://www.securitylab.ru/news/page1_1.php','https://www.securitylab.ru/news/page1_2.php','https://www.securitylab.ru/news/page1_3.php','https://www.securitylab.ru/news/page1_4.php','https://www.securitylab.ru/news/page1_5.php'],
     'linkSelector': 'a.article-card.inline-card',
     'settings': articles.Settings(
    headerSelector="h1.page-title", 
    sourceName="securitylab.ru", 
    annotationSelector="div.articl-text p", 
    imageSelector="div.articl-text img",
    textSelector='div[itemprop="description"]', 
    removeSelector="script, style, meta, form, button, footer", 
    dateCallback=securitylabDateFunc)}
    ]


__resultTemplateFile=open("template.html", encoding = 'utf-8')
ResultTemplate = __resultTemplateFile.read().replace("{","{{").replace("}","}}").replace("{{{{","{").replace("}}}}","}")
__resultTemplateFile.close()