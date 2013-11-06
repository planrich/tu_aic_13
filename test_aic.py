import os
import sys
sys.path.append(os.path.abspath('./wsgi'))

import random
import unittest
import json
import aic.app as app
import aic.db as db

class AICTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.application.test_client()
        session = db.Session()

        self.keyword = db.Keyword("Testkeyword" + str(random.randint(0,1000000000)))
        session.add(self.keyword)
        session.commit()

        self.project = db.Project("", "")
        session.add(self.project)
        session.commit()

        self.task = db.Task(self.project, self.keyword, "")
        self.task.answers_requested = 1
        session.add(self.task)
        session.commit()

    def test_post_answer_bad_task(self):
        data = json.dumps({'answer': 'positive', 'user': "testuser"})
        response = self.app.post('/api/task/0/answers', data=data)
        self.assertEquals(response.status_code, 404)

    def test_post_answer_bad_data(self):
        data = "bad_data"
        response = self.app.post('/api/task/%s/answers' % self.task.id, data=data)
        self.assertEquals(response.status_code, 400)

    def test_post_answer(self):
        data = json.dumps({'answer': 'positive', 'user': "testuser"})
        response = self.app.post('/api/task/%s/answers' % self.task.id, data=data)
        self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()