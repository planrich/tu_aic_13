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

def find_keywords(keywords, paragraph):
    found = []
    for keyword in keywords:
        regex = re.compile(keyword.keyword, re.IGNORECASE)
        if regex.search(paragraph.decode('utf-8')):
            found.append(keyword)
    return found 

def process_feed(feed):
    session = db.Session()
    register_feed(feed)
    keywords = session.query(db.Keyword).all()
    for item in feed['items']:
        html = requests.get(item['url']).text
        texts = parse_article(html)

        print("---")
        project = db.Project("yahoo finance", item['url'])
        session.add(project)
        session.commit()

        for text in texts:
            kws = find_keywords(keywords, text)
            if len(kws) > 0:
                for keyword in kws:
                    task = db.Task(project,keyword,text)
                    session.add(task)
                    session.commit()

                    posted_count = crowd.post(settings.POST_TASK_LINK, task, keyword.keyword)
                    if posted_count > 0:
                        task.posted_count = posted_count
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
