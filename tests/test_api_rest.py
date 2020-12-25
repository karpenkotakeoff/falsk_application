import unittest
import json
from app import app

report_cases = [("json", "application/json",), ("xml", "application/xml",)]
driver_cases = [("SVF", [2, 'Sebastian Vettel', 'FERRARI', '1:12.415'], 200,),
                ("XXX", ['ERROR, abbreviation - "XXX" does not exist'], 404,)]


class ApiTestCase(unittest.TestCase):

    def test_response_report(self):
        tester = app.test_client()
        for format, content_type in report_cases:
            with self.subTest(format=format):
                params = {"format": format}
                response = tester.get("/api/v1/report", query_string=params, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, content_type)

    def test_driver_info(self):
        tester = app.test_client()
        for driver_id, expected, status_code in driver_cases:
            with self.subTest(driver_id=driver_id, status_code=status_code):
                params = {"driver_id": driver_id}
                response = tester.get("/api/v1/report/drivers", query_string=params, follow_redirects=True)
                driver_data = json.loads(response.data)["data"]
                self.assertEqual(response.status_code, status_code)
                self.assertEqual(driver_data, expected)


def test_response_drivers_order(asc_list_drivers):
    tester = app.test_client()
    params = {"order": "asc"}
    response = tester.get("/api/v1/report/drivers", query_string=params, follow_redirects=True)
    asc_list = json.loads(response.data)["data"]
    assert asc_list == asc_list_drivers
    params = {"order": "desc"}
    response = tester.get("/api/v1/report/drivers", query_string=params, follow_redirects=True)
    desc_list = json.loads(response.data)["data"]
    assert asc_list[::-1] == desc_list
