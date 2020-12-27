import argparse
import report_pkg
from unittest import mock


def test_typical_build_report(drivers_data):
    with mock.patch('builtins.open') as patched_open:
        patched_open.side_effect = [mock.mock_open(read_data=text)() for text in drivers_data["input_data"]]
        assert report_pkg.build_report("data") == drivers_data["report"]


def test_argparse():
    a = ["--file", "data", "driver", "Sebastian Vettel"]
    assert report_pkg.input_from_argparse(a) == argparse.Namespace(asc=False, desc=False,
                                                                   driver="Sebastian Vettel", file="data")


def test_print_report_asc(asc_list):
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*asc_list[0])
        assert patched_print.call_args_list == asc_list[1]


def test_print_report_desc(desc_list):
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*desc_list[0])
        assert patched_print.call_args_list == desc_list[1]


def test_print_report_vettel(driver_vettel):
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*driver_vettel[0])
        assert patched_print.call_args_list == driver_vettel[1]
