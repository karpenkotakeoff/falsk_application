import pytest
from unittest import mock
import peewee
from models import Pilots, Qualifications
from parse_data import add_data_to_pilots_table, add_data_to_qualifications_table


@pytest.fixture(scope="class")
def prepare_db():
    MODELS = [Pilots, Qualifications]
    test_db = peewee.SqliteDatabase(":memory:")
    test_db.bind(MODELS)
    test_db.connect()
    test_db.create_tables(MODELS)
    yield
    test_db.drop_tables(MODELS)
    test_db.close()


@pytest.mark.usefixtures("prepare_db", "pilots_info", "qualification_info")
class TestModelsClass:
    def test_add_data_to_pilots_table(self, pilots_info):
        add_data_to_pilots_table(pilots_info)
        assert Pilots.select().count() == 3

    def test_duplicate_add_data_to_pilots_table(self, pilots_info):
        duplicate_pilot = pilots_info[0]
        with mock.patch('builtins.print') as patched_print:
            add_data_to_pilots_table([duplicate_pilot])
        assert patched_print.call_args == mock.call('ERROR, DRR - UNIQUE constraint failed: pilots.abbreviation')

    def test_add_data_to_qualifications_table(self, qualification_info):
        add_data_to_qualifications_table(qualification_info, 2018, "Monaco")
        assert Qualifications.select().count() == 3

    def test_duplicate_add_data_to_qualifications_table(self, qualification_info):
        duplicate_info = qualification_info[0]
        with mock.patch('builtins.print') as patched_print:
            add_data_to_pilots_table([duplicate_info])
        assert patched_print.call_args == mock.call('ERROR, LHM - UNIQUE constraint failed: pilots.abbreviation')
