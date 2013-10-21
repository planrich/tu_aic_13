
import flask
from flask import Flask, g
import psycopg2 as postgres
import time
import requests
import xml.etree.ElementTree as ET
import datetime

shutdown = False

app = Flask(__name__)

@app.before_request
def before_request(request):
    flask.g.db = postgres.connect("dbname=aic user=aic password=aic")

@app.teardown_request
def teardown_request(exception):
    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()

def fetch(url):
    while not shutdown:
        print("fetching from %s" % url)
        rss_req = requests.get(url)
        print("got %d with response type %s" % (rss_req.status_code, rss_req.headers['content-type']))
        print("")

        rss = ET.fromstring(rss_req.text.encode('utf-8'))

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







        time.sleep(30)
