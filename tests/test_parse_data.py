from unittest import mock
from parse_data import parse_pilots_info, parse_qualification_info


def test_parse_pilots_info(raw_data, pilots_info):
    abbreviation = raw_data[0]
    with mock.patch('builtins.open') as patched_open:
        patched_open.side_effect = [mock.mock_open(read_data=abbreviation)()]
        assert parse_pilots_info("folder") == pilots_info


def test_parse_qualification_info(raw_data, qualification_info):
    end = raw_data[1]
    start = raw_data[2]
    with mock.patch('builtins.open') as patched_open:
        patched_open.side_effect = [mock.mock_open(read_data=text)() for text in [end, start]]
        assert parse_qualification_info("folder") == qualification_info
