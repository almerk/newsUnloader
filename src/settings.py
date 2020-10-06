import articles

DAYS_INTERVAL=7
ARTICLE_TEMPLATE='''
<article> 
    <header>{header}</header>
    <p class="annotation">{annotation}</p>
    <figure> <img src="{imgEncoded}"> </figure>
    <section>{text}</section>
    <footer>{source}, {date:%d.%m.%Y}</footer>
</article>'''
def xakepDateFunc(article, soup):
    article.date=articles.getDateFromString(article.url)

SOURCES = [
    {'url':'https://xakep.ru/',
     'linkSelector': '.bd-main .entry-title > a',
     'settings': articles.Settings(
    headerSelector="h1.post-title", 
    sourceName="xakep.ru", 
    annotationSelector="article.post p", 
    imageSelector="a.bdaia-featured-img-cover",
    textSelector="article.post", 
    removeSelector="script, style, meta, form, button, footer, div#current_issue_box", 
    dateCallback=xakepDateFunc)}
    ]

 
__resultTemplateFile=open("template.html", encoding = 'utf-8')
ResultTemplate = __resultTemplateFile.read()
__resultTemplateFile.close()