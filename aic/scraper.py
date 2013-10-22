import psycopg2 as postgres
import requests
import xml.etree.ElementTree as ET
import settings

db = postgres.connect(**settings.DB)

def fetch(url=settings.RSS_URL):
    print("fetching from %s" % url)
    rss_req = requests.get(url)
    print("got %d with response type %s" % (rss_req.status_code, rss_req.headers['content-type']))
    print("")
    return ET.fromstring(rss_req.text.encode('utf-8'))

def process(rss):
    #print(ET.tostring(rss))
    last_build_date_element = rss.find("./channel/pubDate")
    # parse into date time and compare with the last fetch (from db) if something has changed...
    print("last build date: %s" % last_build_date_element.text)

    for item in rss.findall('.//item'):
        title = item.find('./title').text
        link = item.find('./link').text
        pubDate = item.find('./pubDate').text
        print("Title: %s" % title)

        # TODO persist into database and create mobile work tasks

if __name__ == "__main__":
    rss = fetch()
    process(rss)