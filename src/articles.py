import requests
from bs4 import BeautifulSoup
import re


class Settings:
    def __init__(self, headerSelector, source, annotationSelector, imageSelector, textSelector,  dateCallback=None):
        self.headerSelector = headerSelector
        self.source = source,
        self.annotationSelector = annotationSelector
        self.imageSelector = imageSelector
        self.textSelector = textSelector
        self.dateCallback = dateCallback
class Article:
    def __init__(self, url, settings):
        self.url = url
        self.__settings = settings
        self.__parse()
    def __parse(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "lxml")
        self.header = soup.select_one(self.__settings.headerSelector).text
        self.source = self.__settings.source
        self.annotation = soup.select_one(
            self.__settings.annotationSelector).text
        self.imageUrl = self.__find_url(
            str(soup.select_one(self.__settings.imageSelector)))
        self.text = self.__cleanup(soup.select_one(self.__settings.textSelector)).prettify()
    def __find_url(self, text):
        result = re.search(
            r'''https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)''', text)
        return result.group(0)
    def __cleanup(self, soup):
        for s in soup.select("script, style, meta, form, button"):
            s.extract()
        return soup