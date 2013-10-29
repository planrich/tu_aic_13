from flask import Flask, request
import platform
import db

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

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
	return "a"

if __name__ == "__main__":
    application.debug = True
    application.run()
