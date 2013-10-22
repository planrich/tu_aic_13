import flask
import psycopg2 as postgres
import settings

app = flask.Flask(__name__)
db = postgres.connect(**settings.DB)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()