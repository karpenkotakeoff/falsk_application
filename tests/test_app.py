import unittest
from app import app

urls_headlines = [("/", b"Report"), ("/report/", b"Report"), ("/report/drivers/", b"Drivers List")]


class AppTestCase(unittest.TestCase):

    def test_response_pages(self):
        tester = app.test_client()
        for url, headline in urls_headlines:
            with self.subTest(url=url):
                response = tester.get(url, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(headline, response.data)
