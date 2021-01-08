import peewee
import os
from models import Pilots, Qualifications
from utils import parse_laptimes


abbreviations = "abbreviations.txt"
end = "end.log"
start = "start.log"


def parse_pilots_info(folder):
    pilots_info = []
    with open(os.path.join(folder, abbreviations)) as abb_file:
        for line in abb_file.read().split("\n"):
            abbreviation, name, team = line.split("_")
            pilots_info.append((abbreviation, name, team,))
    return pilots_info


def add_data_to_pilots_table(pilots_info):
    for pilot in pilots_info:
        abbreviation, name, team = pilot
        try:
            Pilots.create(abbreviation=abbreviation, name=name, team=team)
        except peewee.IntegrityError as e:
            print(f"ERROR, {abbreviation} - {e}")


def parse_qualification_info(folder):
    qualification_info = []
    with open(os.path.join(folder, end))as end_file:
        lap_times_end = parse_laptimes(end_file)
    with open(os.path.join(folder, start)) as start_file:
        lap_times_start = parse_laptimes(start_file)
    for abbreviation, end_lap in lap_times_end.items():
        start_lap = lap_times_start[abbreviation]
        qualification_info.append((abbreviation, start_lap, end_lap,))
    return qualification_info


def add_data_to_qualifications_table(qualification_info, season, grand_prix):
    pilots_table = Pilots.select()
    pilots = {}
    for pilot in pilots_table:
        pilots[pilot.abbreviation] = pilot
    for pilot in qualification_info:
        abbreviation, start_lap, end_lap = pilot
        try:
            Qualifications.create(pilot=pilots[abbreviation], start_lap=start_lap, end_lap=end_lap,
                                  season=season, grand_prix=grand_prix)
        except peewee.IntegrityError as e:
            print(f"ERROR, {abbreviation} - {e}")


if __name__ == "__main__":
    path_to_data = os.path.join(os.path.dirname(__file__), "../data")
    data_folder = os.path.normpath(path_to_data)
    pilots_info = parse_pilots_info(data_folder)
    qualification_info = parse_qualification_info(data_folder)
    add_data_to_pilots_table(pilots_info)
    add_data_to_qualifications_table(qualification_info, 2018, "Monaco")
