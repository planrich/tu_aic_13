import settings
import requests
import xml.etree.ElementTree as ET
import dateutil.parser
from lxml import etree
from StringIO import StringIO
import db
import json
import crowd
import re

TEXT_SIZE = 250

def fetch_rss(url):
    try:
        response = requests.get(url)
        return ET.fromstring(response.text.encode('utf-8'))
    except Exception as e:
        return None

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

def find_keywords(patterns, paragraph):
    found = []
    for keyword, pattern in patterns:
        if pattern.search(paragraph.decode('utf-8')):
            found.append(keyword)
    return found

def process_feed(feed):
    session = db.Session()
    register_feed(feed)
    keywords = session.query(db.Keyword).all()
    for item in feed['items']:
        print("---")
        print("getting article %s" % item['url'])
        html = requests.get(item['url']).text
        texts = parse_article(html)

        project = db.Project("yahoo finance", item['url'])
        session.add(project)
        session.commit()

        patterns = [ (keyword, re.compile(r"\b({0})\b".format(keyword.keyword), flags=re.IGNORECASE|re.LOCALE)) for keyword in keywords ]

        print("searching %d paragraphs" % (len(texts),))
        for text in texts:
            kws = find_keywords(patterns, text)
            if len(kws) > 0:
                for keyword in kws:
                    task = db.Task(project,keyword,text)
                    session.add(task)
                    session.commit()

                    answers_requested = crowd.post_task(task, keyword)
                    if answers_requested > 0:
                        task.answers_requested = answers_requested
                        session.commit()
                        print('task (id: %d) created, keyword: %s' % (task.id,keyword.keyword))
                    else:
                        print('task was not created')
                        session.delete(task)
                        session.commit()

        if len(project.tasks) == 0:
            print("no task posted. removing project")
            session.delete(project)
            session.commit()
        else:
            print("project with %d tasks created" % len(project.tasks))

    print("closing session")
    session.close()


def register_feed(feed):
    session = db.Session()
    pub = db.Publication(feed['date'])
    session.add(pub)
    session.commit()
    session.close()


def parse_article(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    ps = tree.xpath("//div[@id='mediablogbody' or @itemprop='articleBody']/div/p")
    if len(ps) == 0:
        # i believe that they build their pages against anti scraping ^^
        ps = tree.xpath("//div[@class='body yom-art-content clearfix']/p")
        
    texts = []
    text = ''
    for p in ps:
        p_text = etree.tostring(p, encoding="utf-8", method="text")
        # they include some related articles which are not very interesting for us
        if not p_text.startswith("Related:"):
            text += '\n' + p_text if text else p_text
            if len(text) > TEXT_SIZE:
                texts.append(text)
                text = ''
    print texts
    return texts


if __name__ == '__main__':
    rss = fetch_rss(settings.RSS_URL)
    feed = parse_rss(rss)
    try:
        if not is_feed_processed(feed):
            process_feed(feed)
    except requests.exceptions.ConnectionError as e:
        print("failed to process feed due to " + str(e))
