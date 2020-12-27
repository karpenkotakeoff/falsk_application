import peewee
import os
from models import Pilots, Qualifications
from report_pkg import parse_laptimes


abbreviations = "abbreviations.txt"
end = "end.log"
start = "start.log"


def parse_pilots_info(folder):
    with open(os.path.join(folder, abbreviations)) as abb_file:
        for line in abb_file.read().split("\n"):
            abbreviation, name, team = line.split("_")
            try:
                Pilots.create(abbreviation=abbreviation, name=name, team=team)
            except peewee.IntegrityError as e:
                print(f"ERROR, {abbreviation} - {e}")


def parse_qualification_info(folder, season, grand_prix):
    with open(os.path.join(folder, end))as end_file:
        lap_times_end = parse_laptimes(end_file)
    with open(os.path.join(folder, start)) as start_file:
        lap_times_start = parse_laptimes(start_file)
    for abbreviation, end_lap in lap_times_end.items():
        pilot = Pilots.select().where(Pilots.abbreviation == abbreviation).get()
        start_lap = lap_times_start[abbreviation]
        try:
            Qualifications.create(pilot=pilot, start_lap=start_lap, end_lap=end_lap,
                                  season=season, grand_prix=grand_prix)
        except peewee.IntegrityError as e:
            print(f"ERROR, {abbreviation} - {e}")


if __name__ == "__main__":
    path_to_data = os.path.join(os.path.dirname(__file__), "../data")
    data_folder = os.path.normpath(path_to_data)
    parse_pilots_info(data_folder)
    parse_qualification_info(data_folder, 2018, "Monaco")
