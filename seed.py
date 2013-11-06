import os
import sys
sys.path.append(os.path.abspath('./wsgi'))

import aic.db as db

session = db.Session()

keyword = db.Keyword("Apple")
session.add(keyword)

keyword = db.Keyword("Microsoft")
session.add(keyword)

keyword = db.Keyword("Facebook")
session.add(keyword)

keyword = db.Keyword("General Motors")
session.add(keyword)

keyword = db.Keyword("Google")
session.add(keyword)

keyword = db.Keyword("Yahoo")
session.add(keyword)

keyword = db.Keyword("Western Union")
session.add(keyword)

keyword = db.Keyword("JP Morgan")
session.add(keyword)

keyword = db.Keyword("NSA")
session.add(keyword)

keyword = db.Keyword("ECB")
session.add(keyword)

session.commit()
session.close()