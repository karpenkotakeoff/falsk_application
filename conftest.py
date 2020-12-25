import pytest
import report_pkg
import datetime
from unittest import mock


@pytest.fixture
def drivers_data():
    abbreviations = """DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
LHM_Lewis Hamilton_MERCEDES"""
    end = """LHM2018-05-24_12:19:32.585
SVF2018-05-24_12:04:11.332
DRR2018-05-24_12:12:36.080"""
    start = """SVF2018-05-24_12:02:58.917
DRR2018-05-24_12:11:24.067
LHM2018-05-24_12:18:20.125"""
    report = [report_pkg.PilotStats(abbreviation="DRR",
                                    name='Daniel Ricciardo', team='RED BULL RACING TAG HEUER',
                                    fastest_lap=datetime.timedelta(seconds=72, microseconds=13000)),
              report_pkg.PilotStats(abbreviation="SVF",
                                    name='Sebastian Vettel', team='FERRARI',
                                    fastest_lap=datetime.timedelta(seconds=72, microseconds=415000)),
              report_pkg.PilotStats(abbreviation="LHM",
                                    name='Lewis Hamilton', team='MERCEDES',
                                    fastest_lap=datetime.timedelta(seconds=72, microseconds=460000))]
    separator = "-" * 70
    print_asc = [
        mock.call(" 1. Daniel Ricciardo    | RED BULL RACING TAG HEUER     | 1:12.013"),
        mock.call(" 2. Sebastian Vettel    | FERRARI                       | 1:12.415"),
        mock.call(" 3. Lewis Hamilton      | MERCEDES                      | 1:12.460"),
        mock.call(separator)]
    print_vettel = [mock.call(" 2. Sebastian Vettel    | FERRARI                       | 1:12.415")]

    data = {
        "report": report,
        "print_asc": print_asc,
        "print_vettel": print_vettel,
        "input_data": [abbreviations, end, start]
    }
    return data


@pytest.fixture
def asc_list(drivers_data):
    report = drivers_data["report"]
    driver = None
    desc = False
    params = (report, driver, desc)
    expected = drivers_data["print_asc"]
    return params, expected


@pytest.fixture
def desc_list(drivers_data):
    report = drivers_data["report"]
    driver = None
    desc = True
    params = (report, driver, desc)
    expected = drivers_data["print_asc"][::-1]
    return params, expected


@pytest.fixture
def driver_vettel(drivers_data):
    report = drivers_data["report"]
    driver = "Sebastian Vettel"
    desc = False
    params = (report, driver, desc)
    expected = drivers_data["print_vettel"]
    return params, expected


@pytest.fixture
def asc_list_drivers():
    asc_list = [['DRR', 'Daniel Ricciardo'], ['SVF', 'Sebastian Vettel'],
                ['VBM', 'Valtteri Bottas'], ['LHM', 'Lewis Hamilton'],
                ['SVM', 'Stoffel Vandoorne'], ['KRF', 'Kimi Räikkönen'],
                ['FAM', 'Fernando Alonso'], ['SSW', 'Sergey Sirotkin'],
                ['CLS', 'Charles Leclerc'], ['SPF', 'Sergio Perez'],
                ['RGH', 'Romain Grosjean'], ['PGS', 'Pierre Gasly'],
                ['CSR', 'Carlos Sainz'], ['EOF', 'Esteban Ocon'],
                ['NHR', 'Nico Hulkenberg'], ['BHS', 'Brendon Hartley'],
                ['MES', 'Marcus Ericsson'], ['LSW', 'Lance Stroll'],
                ['KMH', 'Kevin Magnussen']]
    return asc_list
