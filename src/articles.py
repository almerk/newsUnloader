import requests
from bs4 import BeautifulSoup
import re
import base64


class Settings:
    def __init__(self, headerSelector, source, annotationSelector, imageSelector, textSelector,  dateCallback=None, removeSelector="script, style, meta, form, button"):
        self.headerSelector = headerSelector
        self.source = source,
        self.annotationSelector = annotationSelector
        self.imageSelector = imageSelector
        self.textSelector = textSelector
        self.dateCallback = dateCallback
        self.removeSelector=removeSelector
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
        self.text = self.__cleanup(soup.select_one(self.__settings.textSelector))
    def __find_url(self, text):
        result = re.search(
            r'''https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)''', text)
        return result.group(0)
    def __cleanup(self, soup):
        for s in soup.select(self.__settings.removeSelector):
            s.extract()
        for s in soup.select("a"):
            s.unwrap()
        return str(soup.prettify())
    def imageUrl2Base64(self, url):
        print("Getting image ", url)
        req = requests.get(url, stream=True)
        req.raise_for_status()
        chunks=bytearray()
        for chunk in req.iter_content(chunk_size=50000):
            chunks+=chunk
        return base64.b64encode(chunks)