class Article(object):
    def __init__(self, url, title, pub_date, plaintext):
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.plaintext = plaintext

    def paragraphs(self):
        return [] # TODO

