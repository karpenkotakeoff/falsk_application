import os
from dict2xml import dict2xml
from flask import Blueprint, make_response
from flask_restful import Api, Resource, reqparse
from report_pkg import build_report, format_delta, create_printer

api_bp = Blueprint("api_app", __name__, url_prefix="/api/v1")
api = Api(api_bp)

path_to_data = os.path.join(os.path.dirname(__file__), "../../data")
data_folder = os.path.normpath(path_to_data)

report = build_report(data_folder)
printer = create_printer(report)

parser_report = reqparse.RequestParser()
parser_report.add_argument("format", type=str)

parser_drivers = reqparse.RequestParser()
parser_drivers.add_argument("format", type=str)
parser_drivers.add_argument("order", type=str)
parser_drivers.add_argument("driver_id", type=str)


def render_response(response, response_format=None, status_code=200):
    if response_format == "xml":
        response = make_response(dict2xml({"data": response}, wrap="response"), status_code)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return make_response({"data": response}, status_code)


class Report(Resource):
    def get(self):
        """
        file: report.yml
        """
        args = parser_report.parse_args()
        response_format = args["format"]
        response = []
        for position, driver in printer:
            response.append([driver.abbreviation, position, driver.name,
                             driver.team, format_delta(driver.fastest_lap)])
        return render_response(response, response_format)


def build_response(printer, order="asc"):
    response = []
    for position, driver in printer:
        response.append([driver.abbreviation, driver.name])
    if order == "desc":
        response = response[::-1]
    return response


def build_driver_response(printer, driver_id):
    response = []
    for position, driver in printer:
        if driver.abbreviation == driver_id:
            response = [position, driver.name, driver.team, format_delta(driver.fastest_lap)]
    return response


class Drivers(Resource):
    def get(self):
        """
        file: drivers.yml
        """
        args = parser_drivers.parse_args()
        response_format = args["format"]
        order = args["order"]
        driver_id = args["driver_id"]
        if driver_id:
            if driver_id in {driver.abbreviation for driver in report}:
                response = build_driver_response(printer, driver_id)
                return render_response(response, response_format)
            else:
                response = [f'ERROR, abbreviation - "{driver_id}" does not exist']
                return render_response(response, response_format, status_code=404)
        response = build_response(printer, order)
        return render_response(response, response_format)


api.add_resource(Report, "/report/")
api.add_resource(Drivers, "/report/drivers/")
