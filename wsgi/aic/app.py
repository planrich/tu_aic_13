from flask import Flask
import platform
application = Flask(__name__)

@application.route("/")
def index():
    return 'Hello from Flask(1)'

@application.route("/info")
def info():
    return platform.python_version()

if __name__ == "__main__":
    app.debug = True
    app.run()
