import flask
import psycopg2 as postgres

app = flask.Flask(__name__)
db = postgres.connect("dbname=aic user=aic password=aic host=127.0.0.1")

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()