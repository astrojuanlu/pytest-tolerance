"""
Large parts of this code are inspired by
https://github.com/pytest-dev/pytest-rerunfailures/
"""

import random

import pytest

from _pytest.runner import runtestprotocol


def pytest_configure(config):
    """Add tolerance marker."""
    config.addinivalue_line(
        "markers", "tolerance(): mark test to try tolerance values."
    )


def pytest_runtest_protocol(item, nextitem):
    """Controls how tests are rerun."""
    marked = item.get_closest_marker("tolerance")
    if marked is None:
        return

    need_to_run = True
    while need_to_run:
        item.ihook.pytest_runtest_logstart(nodeid=item.nodeid, location=item.location)

        # Run test
        # but do not log failed attempts just yet
        reports = runtestprotocol(item, log=False, nextitem=nextitem)

        for report in reports:  # 3 reports: setup, call, teardown
            if report.failed:
                # I must rerun the test
                report.outcome = "rerun"
                item.ihook.pytest_runtest_logreport(report=report)
                break
            else:
                # Test passed, log normally
                item.ihook.pytest_runtest_logreport(report=report)

        else:
            # All the reports were successful, no need to rerun the test
            need_to_run = False

        item.ihook.pytest_runtest_logfinish(nodeid=item.nodeid, location=item.location)

    return True


def pytest_report_teststatus(report):
    if report.outcome == "rerun":
        return "rerun", "R", ("RERUN", {"yellow": True})


@pytest.fixture(scope="function")
def tolerance(request):
    value = 1 * 10 ** random.randint(-20, 0)
    return value
