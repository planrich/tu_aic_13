import os, sys
sys.path.append(os.path.abspath('./wsgi'))

import unittest
import aic.app

class AICTestCase(unittest.TestCase):
    def setUp(self):
        self.app = aic.app.application.test_client()

    def test_post_webhook_with_malformed_data(self):
        data = "bad_data"
        response = self.app.post('/webhook', data=data)
        self.assertEquals(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()