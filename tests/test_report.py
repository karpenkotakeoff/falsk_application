import argparse
import report_pkg
from unittest import mock


def test_typical_build_report(raw_data, short_report):
    with mock.patch('builtins.open') as patched_open:
        patched_open.side_effect = [mock.mock_open(read_data=text)() for text in raw_data]
        assert report_pkg.build_report("data") == short_report


def test_argparse():
    a = ["--file", "data", "driver", "Sebastian Vettel"]
    assert report_pkg.input_from_argparse(a) == argparse.Namespace(asc=False, desc=False,
                                                                   driver="Sebastian Vettel", file="data")


def test_print_report_asc(asc_list):
    params = asc_list[0]
    expected = asc_list[1]
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*params)
        assert patched_print.call_args_list == expected


def test_print_report_desc(desc_list):
    params = desc_list[0]
    expected = desc_list[1]
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*params)
        assert patched_print.call_args_list == expected


def test_print_report_vettel(driver_vettel):
    params = driver_vettel[0]
    expected = driver_vettel[1]
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*params)
        assert patched_print.call_args_list == expected
