from dict2xml import dict2xml
from flask import make_response
from models import Qualifications
from dataclasses import dataclass
import datetime


@dataclass
class PilotStats:
    abbreviation: str
    name: str
    team: str
    fastest_lap: datetime.timedelta


def format_delta(lap_timedelta):
    milliseconds = round(lap_timedelta.microseconds / 1000)
    sec = lap_timedelta.seconds
    minutes, seconds = divmod(sec, 60)
    string = "{}:{}.{:03d}".format(minutes, seconds, milliseconds)
    return string


def parse_laptimes(file_for_parsing):
    lap_times = {}
    for line in file_for_parsing.read().split("\n"):
        abbreviation = line[:3]
        end_datetime = line[3:]
        lap_times[abbreviation] = datetime.datetime.fromisoformat(end_datetime)
    return lap_times

def create_printer(report_list):
    printer = []
    for position, line in enumerate(report_list, 1):
        printer.append((position, line,))
    return printer


def make_report_from_db():
    report = []
    query = Qualifications.select(Qualifications.pilot, Qualifications.end_lap, Qualifications.start_lap)
    for row in query:
        abbreviation = row.pilot.abbreviation
        name = row.pilot.name
        team = row.pilot.team
        fastest_lap = row.end_lap - row.start_lap
        report.append(PilotStats(abbreviation, name, team, fastest_lap))
    report.sort(key=lambda i: i.fastest_lap)
    return report


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


def render_response(response, response_format=None, status_code=200):
    if not response_format or response_format == "json":
        return make_response({"data": response}, status_code)
    elif response_format == "xml":
        response = make_response(dict2xml({"data": response}, wrap="response"), status_code)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return f'Sorry, format - "{response_format}" does not support'
