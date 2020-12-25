import datetime
import argparse
import sys
import os
from dataclasses import dataclass


@dataclass
class PilotStats:
    abbreviation: str
    name: str
    team: str
    fastest_lap: datetime.timedelta


abbreviations = "abbreviations.txt"
end = "end.log"
start = "start.log"


def parse_laptimes(file_for_parsing):
    lap_times = {}
    for line in file_for_parsing.read().split("\n"):
        abbreviation = line[:3]
        end_datetime = line[3:]
        lap_times[abbreviation] = datetime.datetime.fromisoformat(end_datetime)
    return lap_times


def build_report(file):
    """
    Take params and returned report of qualification

    :param file: folder path
    :return: report list
    """
    pilots = {}
    report = []
    with open(os.path.join(file, abbreviations)) as abb_file:
        for line in abb_file.read().split("\n"):
            abbreviation, name, team = line.split("_")
            pilots[abbreviation] = (name, team,)
    with open(os.path.join(file, end))as end_file:
        lap_times_end = parse_laptimes(end_file)
    with open(os.path.join(file, start)) as start_file:
        lap_times_start = parse_laptimes(start_file)
    for abbreviation, start_time in lap_times_start.items():
        end_time = lap_times_end[abbreviation]
        fastest_lap = end_time - start_time
        pilots[abbreviation] += (fastest_lap,)
    sorted_laps = list(pilots.items())
    sorted_laps.sort(key=lambda i: i[1][2])
    for abbreviation, abbr_driver_tuple in sorted_laps:
        name, team, fastest_lap = abbr_driver_tuple
        report.append(PilotStats(abbreviation, name, team, fastest_lap))
    return report


def format_delta(lap_timedelta):
    milliseconds = round(lap_timedelta.microseconds / 1000)
    sec = lap_timedelta.seconds
    minutes, seconds = divmod(sec, 60)
    string = "{}:{}.{:03d}".format(minutes, seconds, milliseconds)
    return string


def create_printer(report_list):
    printer = []
    for position, line in enumerate(report_list, 1):
        printer.append((position, line,))
    return printer


def print_report(report, driver=None, desc=False):
    """
    Print report to stdout

    :param report: report of qualification result
    :param driver: name of driver whose statistic you wish to show
    :param desc: order descending
    :return: None
    """
    separator = "-" * 70
    if driver:
        printer = []
        for position, line in enumerate(report, 1):
            if line.name == driver:
                printer.append((position, line,))
    elif desc:
        separator_line_num = -15
        printer = create_printer(report)[::-1]
        printer.insert(separator_line_num, separator)
    else:
        separator_line_num = 15
        printer = create_printer(report)
        printer.insert(separator_line_num, separator)
    for item in printer:
        if isinstance(item, str):
            print(item)
        else:
            position, line = item
            print("{:>2}. {:<20}| {:<30}| {}".format(position, line.name, line.team, format_delta(line.fastest_lap)))


def input_from_argparse(cl_args):
    """
    Parse args from command line

    :return: args
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands',
                                       help='Name of driver whose statistics you wish to watch')
    parser.add_argument("-f", "--file", type=str, help="Folder path")
    parser_driver = subparsers.add_parser("driver", help="Name")
    parser_driver.add_argument("driver", type=str)
    group.add_argument("--asc", action="store_true", help="Order by time asc")
    group.add_argument("--desc", action="store_true", help="Order by time desc")
    args = parser.parse_args(cl_args)
    return args


def main():
    """
    Main func 

    :return: none
    """
    args = input_from_argparse(sys.argv[1:])
    report = build_report(args.file)
    if "driver" in args:
        print_report(report, driver=args.driver)
    else:
        print_report(report, desc=args.desc)


if __name__ == "__main__":
    main()
