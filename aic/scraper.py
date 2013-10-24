import psycopg2 as postgres
import requests
import xml.etree.ElementTree as ET
import settings
from dateutil.parser import parse
from lxml import etree
from StringIO import StringIO
import re

db = postgres.connect(**settings.DB)

def rss_date(date_str):
    return parse(date_str)

def fetch(url=settings.RSS_URL):
    print("fetching from %s" % url)
    rss_req = requests.get(url)
    print(" -> got %d with response type %s" % (rss_req.status_code, rss_req.headers['content-type']))
    return ET.fromstring(rss_req.text.encode('utf-8'))

def fetch_article(url):
    print("fetching article '%s'" % url)
    html_req = requests.get(url)
    print(" -> got %d with response type %s" % (html_req.status_code, html_req.headers['content-type']))
    if html_req.status_code != 200:
        return None

    return html_req.text.encode('utf-8')

def process_article(html):
    if html is None:
        return None

    html_parser = etree.HTMLParser()
    html_tree = etree.parse(StringIO(html), html_parser)

    text_div = html_tree.xpath("//div[@id='mediaarticlebody' or @itemprop='articleBody']")[0]
    for paragraph in text_div.xpath("./div/p/text()"):
        paragraph_normalized = re.sub(r"(\s|\n){2,}", r" ", paragraph)
        print(str(paragraph.encode('utf-8')))
        print("")
        break

    return None

def process(rss):
    #print(ET.tostring(rss))
    last_build_date_element = rss.find("./channel/pubDate")
    # parse into date time and compare with the last fetch (from db) if something has changed...
    print("last build date: %s" % last_build_date_element.text)
    last_build_date = rss_date(last_build_date_element.text)

    for item in rss.findall('.//item'):
        title = item.find('./title').text
        link = item.find('./link').text
        pubDate = rss_date(item.find('./pubDate').text)
        print("Title: %s" % title)

        html = fetch_article(link)
        plain_text = process_article(html)
        break

        # TODO persist into database and create mobile work tasks

if __name__ == "__main__":
    rss = fetch()
    process(rss)
