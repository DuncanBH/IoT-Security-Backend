import unittest
from PostAPi import app

class SendDummyData(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def send_detected_data(self):
        response = self.app.post("/api/sound",
                                 headers={"Content-Type": "application/json"},
                                 data={"soundAvg": 700})

