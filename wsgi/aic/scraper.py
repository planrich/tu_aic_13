import requests
import xml.etree.ElementTree as ET
import settings
from dateutil.parser import parse
from lxml import etree
from StringIO import StringIO
import re
import db
import datetime
import sqlalchemy
import pytz

def rss_date(date_str):
    date = parse(date_str)
    return date.replace(tzinfo=None)

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

    # some rare articles have an additional wrapping, so unwarp that here
    if text_div.xpath("count(div/p)") == 0:
        text_div = text_div.xpath("div[@class='bd']")[0]

    paragraphs = []
    for node in text_div.xpath("div/p"):
        paragraph = etree.tostring(node, encoding="utf-8", method="text")
        # they include some related articles which are not very interesting for us
        # -> filtered
        if paragraph.startswith("Related:"):
            continue
        paragraphs.append(paragraph)

    print("found %d" % len(paragraphs))
    return paragraphs

def process(rss, session):
    #print(ET.tostring(rss))
    last_build_date_element = rss.find("./channel/pubDate")
    # parse into date time and compare with the last fetch (from db) if something has changed...
    last_build_date = rss_date(last_build_date_element.text)
    print("last build date: %s" % last_build_date)

    try:
        last = session.query(db.Publication).one()
        print("# last was publication date was: %s" % last_build_date)
    except sqlalchemy.orm.exc.NoResultFound:
        last = db.Publication(datetime.datetime(1970,1,1))
        session.add(last)

    last_pub_date = last.datetime

    for item in rss.findall('.//item'):
        title = item.find('./title').text
        link = item.find('./link').text
        pubDate = rss_date(item.find('./pubDate').text)

        if pubDate < last_pub_date:
            continue

        if pubDate > last.datetime:
            print("setting new date: %s" % pubDate)
            last.datetime = pubDate

        html = fetch_article(link)
        paragraphs = process_article(html)

    session.commit()


        # TODO persist into database and create mobile work tasks

if __name__ == "__main__":
    rss = fetch()
    session = db.Session()
    process(rss, session)
