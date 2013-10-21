
import application
import threading

app = application.app

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    print("starting background fetcher")
    thread = threading.Thread(target=application.fetch,\
            name="background_fetcher", args=("http://finance.yahoo.com/news/?format=rss",))
    thread.start();

    app.run()
    application.shutdown = True

    print("joining background fetcher")
    thread.join()
