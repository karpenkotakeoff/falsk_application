from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from report_pkg import format_delta, create_printer
from utils import make_report_from_db, render_response, build_driver_response, build_response

api_bp = Blueprint("api_app", __name__, url_prefix="/api/v1")
api = Api(api_bp)

parser_report = reqparse.RequestParser()
parser_report.add_argument("format", type=str)

parser_drivers = reqparse.RequestParser()
parser_drivers.add_argument("format", type=str)
parser_drivers.add_argument("order", type=str)
parser_drivers.add_argument("driver_id", type=str)


report = make_report_from_db()
printer = create_printer(report)


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
