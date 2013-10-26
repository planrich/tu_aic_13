import settings
import requests
import xml.etree.ElementTree as ET
import dateutil.parser
from lxml import etree
from StringIO import StringIO
import db


TEXT_SIZE = 250


def fetch_rss(url):
    response = requests.get(url)
    return ET.fromstring(response.text.encode('utf-8'))


def parse_date(date_str):
    date = dateutil.parser.parse(date_str)
    return date.replace(tzinfo=None)


def parse_rss(rss):
    feed = { 'date': parse_date(rss.find("./channel/pubDate").text), 'items': [] }
    for i in rss.findall('.//item'):
        title = i.find('./title').text
        url = i.find('./link').text
        date = parse_date(i.find('./pubDate').text)
        feed['items'].append({ 'title': title, 'url': url, 'date': date })
    return feed


def is_feed_processed(feed):
    session = db.Session()
    query = session.query(db.Publication).filter(db.Publication.datetime == feed['date'])
    results = query.all()
    session.close()
    return len(results) != 0


def process_feed(feed):
    register_feed(feed)
    for item in feed['items']:
        html = requests.get(item['url']).text
        texts = parse_article(html)
        ########## TODO: Create tasks in mobile works instead of print the texts
        for text in texts:
            print text
            print '---------------------'


def register_feed(feed):
    session = db.Session()
    pub = db.Publication(feed['date'])
    session.add(pub)
    session.commit()
    session.close()


def parse_article(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    div = tree.xpath("//div[@id='mediaarticlebody' or @itemprop='articleBody']")[0]

    # some rare articles have an additional wrapping, so unwarp that here
    if div.xpath("count(div/p)") == 0:
        div = div.xpath("div[@class='bd']")[0]

    texts = []
    text = ''
    for p in div.xpath("div/p"):
        p_text = etree.tostring(p, encoding="utf-8", method="text")
        # they include some related articles which are not very interesting for us
        if not p_text.startswith("Related:"):
            text += '\n' + p_text if text else p_text
            if len(text) > TEXT_SIZE:
                texts.append(text)
                text = ''
    return texts


if __name__ == '__main__':
    rss = fetch_rss(settings.RSS_URL)
    feed = parse_rss(rss)
    if not is_feed_processed(feed):
        process_feed(feed)