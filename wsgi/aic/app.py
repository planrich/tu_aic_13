from flask import Flask, request
import platform
import db
import os

application = Flask(__name__)

@application.route("/")
def index():
    sess = db.Session()
    pubs = sess.query(db.Publication).all()

    out = 'AIC 2013 crowd sourcing<br/>\n'

    i = 0
    for pub in pubs:
        out += "scrape %d: %s,<br/>\n" % (i,str(pub.datetime))
        i += 1

    return out

@application.route("/info")
def info():
    return platform.python_version()

@application.route("/webhook", methods=['GET', 'POST'])
def webhook():
    folder = os.environ['OPENSHIFT_TMP_DIR']
    if request.method == 'POST':
        data = str(request.stream.read())
        f = open(folder+'/datafile','a')
        f.write(data + ' ### ')
        return '<h1>' + data +'</h1>'

    f = open (folder+'/datafile', 'r')
    return '<p>'+ f.read() +'</p>'

if __name__ == "__main__":
    application.debug = True
    application.run()
