import unittest
from unittest import mock
import peewee
from models import Pilots, Qualifications
from parse_data import parse_pilots_info, parse_qualification_info

MODELS = [Pilots, Qualifications]
test_db = peewee.SqliteDatabase(":memory:")

abbreviations = """DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
LHM_Lewis Hamilton_MERCEDES"""
end = """LHM2018-05-24_12:19:32.585
SVF2018-05-24_12:04:11.332
DRR2018-05-24_12:12:36.080"""
start = """SVF2018-05-24_12:02:58.917
DRR2018-05-24_12:11:24.067
LHM2018-05-24_12:18:20.125"""
season = 2018
grand_prix = "Monaco"
duplicate_pilot_data = """DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER"""
expected_pilot_duplicate = [mock.call("ERROR, DRR - UNIQUE constraint failed: pilots.abbreviation")]
end_duplicate = """DRR2018-05-24_12:12:36.080"""
start_duplicate = """DRR2018-05-24_12:11:24.067"""
expected_quali_duplicate = [mock.call('ERROR, DRR - UNIQUE constraint failed: qualifications.start_lap, qualifications.end_lap')]


class ModelsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_db.bind(MODELS)
        test_db.connect()
        test_db.create_tables(MODELS)

    def test_parsing_pilots_info(self):
        with unittest.mock.patch('builtins.open') as patched_open:
            patched_open.side_effect = [unittest.mock.mock_open(read_data=abbreviations)()]
            exception_flag = parse_pilots_info("folder")
            self.assertEqual(Pilots.select().count(), 3)
        # Duplicate check
        with unittest.mock.patch('builtins.open') as patched_open, mock.patch('builtins.print') as patched_print:
            patched_open.side_effect = [unittest.mock.mock_open(read_data=duplicate_pilot_data)()]
            parse_pilots_info("folder")
            self.assertEqual(Pilots.select().count(), 3)
            self.assertEqual(patched_print.call_args_list, expected_pilot_duplicate)

    def test_parsing_qualification_info(self):
        with unittest.mock.patch('builtins.open') as patched_open:
            patched_open.side_effect = [unittest.mock.mock_open(read_data=log_file)() for log_file in [end, start]]
            parse_qualification_info("folder", season, grand_prix)
            self.assertEqual(Pilots.select().count(), 3)
        # Duplicate check
        with unittest.mock.patch('builtins.open') as patched_open, mock.patch('builtins.print') as patched_print:
            patched_open.side_effect = [unittest.mock.mock_open(read_data=log_string)()
                                        for log_string in [end_duplicate, start_duplicate]]
            parse_qualification_info("folder", season, grand_prix)
            self.assertEqual(Pilots.select().count(), 3)
            self.assertEqual(patched_print.call_args_list, expected_quali_duplicate)

    @classmethod
    def tearDownClass(cls):
        test_db.drop_tables(MODELS)
        test_db.close()
