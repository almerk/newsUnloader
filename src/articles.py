import requests
from bs4 import BeautifulSoup
import re
import base64
from datetime import datetime
from urllib.parse import urljoin


class Settings:
    def __init__(self, headerSelector, sourceName, annotationSelector, imageSelector, textSelector,  dateCallback=None, removeSelector="script, style, meta, form, button", textRemoveSelector=[]):
        self.headerSelector = headerSelector
        self.source = sourceName
        self.annotationSelector = annotationSelector
        self.imageSelector = imageSelector
        self.textSelector = textSelector
        self.dateCallback = dateCallback
        self.removeSelector = removeSelector
        self.textRemoveSelector = textRemoveSelector


class Article:
    def __init__(self, url, settings):
        self.url = url
        self.__settings = settings
        self.date=datetime.today()
        self.__parse()

    def __parse(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "lxml")
        self.header = soup.select_one(self.__settings.headerSelector).text
        self.sourceName = self.__settings.source
        self.annotation = soup.select_one(
            self.__settings.annotationSelector).text
        self.imageUrl = self.__find_url(soup.select_one(self.__settings.imageSelector))
        self.image = imageUrl2Base64(urljoin(self.url, self.imageUrl)) if self.imageUrl !='' else ''
        self.text = self.__cleanup(
            soup.select_one(self.__settings.textSelector))
        if(self.__settings.dateCallback is not None):
            self.__settings.dateCallback(self, soup)

    def __find_url(self, link):
        if(not link.has_attr("src")):
            result = re.search(
                r'''https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)''', str(link))
            return result.group(0) if(result is not None) else ''
        else:
            return link["src"]

    def __cleanup(self, soup):
        print("Cleaning text")
        for s in soup.select(self.__settings.removeSelector):
            s.extract()
        for s in soup.select("a"):
            s.unwrap()
        for tag in soup():
            for attribute in ["class", "id", "name", "style", "srcset"]:
                del tag[attribute]
        for s in soup.select("img"):
            s["src"] = imageUrl2Base64(urljoin(self.url, s["src"]) )
        for r in self.__settings.textRemoveSelector:
            soup.select_one(r).extract()
        return str(soup.prettify())

    def toString(self, template):
        return template.format(header=self.header,
         annotation=self.annotation,
         imgEncoded=self.image,
         text=self.text,
         source=self.sourceName,
         date=self.date)


def imageUrl2Base64(url):
    if url=='':
        return ''
    if not url.startswith("http"):
        return ''
    print("Getting image ", url)
    try:
        req = requests.get(url)
        return "data:" + req.headers['Content-Type'] + ";" + "base64," + base64.b64encode(req.content).decode("utf-8")
    except BaseException:
        return ""
def getDateFromString(s):
    res = re.search(r'''\/\d{4}\/\d{2}\/\d{2}\/''', s)
    dt = datetime.strptime(res.group(0), "/%Y/%m/%d/")
    return dt