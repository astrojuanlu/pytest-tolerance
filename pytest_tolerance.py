"""
General acknowledgements:

* Large parts of this code are inspired by
  https://github.com/pytest-dev/pytest-rerunfailures/
* See also https://github.com/pytest-dev/pytest/issues/3261#issuecomment-369740536
  for a useful representation of the hook order

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
    marker = item.get_closest_marker("tolerance")
    if marker is None:
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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # https://github.com/pytest-dev/pytest/issues/230#issuecomment-223453793
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


FIXTURES_CACHE = {}


def get_fixture(nodeid, *args, **kwargs):
    if nodeid not in FIXTURES_CACHE:
        FIXTURES_CACHE[nodeid] = ToleranceFixture(*args, **kwargs)

    return FIXTURES_CACHE[nodeid]


class ToleranceFixture:
    def __init__(
        self, try_exact=True, min_exponent=-20, max_exponent=0, random_values=False
    ):
        self._try_exact = try_exact
        self._random_values = random_values
        self._min_exponent = min_exponent
        self._max_exponent = max_exponent

        self._last_exponent = None
        self._num_calls = 0
        self._last_failed = None

    def _get_next_exponent_bisection(self):
        # TODO: This is promising but currently useless
        # Once the tests passes we never call the fixture again
        # so we don't have the opportunity
        # to give a more accurate exponent
        if self._last_exponent is None:
            self._last_exponent = (self._min_exponent + self._max_exponent) // 2

        if self._last_failed:
            # Relax the tolerance
            return (self._last_exponent + self._max_exponent) // 2
        else:
            # Tighten the tolerance
            return (self._last_exponent + self._min_exponent) // 2

    def _get_next_exponent_step(self, step=1):
        # TODO: This can potentially make the tests very slow
        if self._last_exponent is None:
            self._last_exponent = self._min_exponent

        return self._last_exponent + step

    def __call__(self):
        if self._random_values:
            # Just return a random value
            value = 10 ** random.randint(self._min_exponent, self._max_exponent)

        elif self._try_exact and self._num_calls == 0:
            # Let's first try the exact comparison
            value = 0.0

        else:
            self._last_exponent = self._get_next_exponent_step()
            value = float(10 ** self._last_exponent)

        self._num_calls += 1
        print(value)
        return value

    def set_last_failed(self, last_failed):
        self._last_failed = last_failed


@pytest.fixture(scope="function")
def tolerance(request):
    item = request.node
    marker = item.get_closest_marker("tolerance")

    if marker is None:
        raise ValueError("Mark the test with @pytest.mark.tolerance()")
    else:
        fixture = get_fixture(item.nodeid, *marker.args, **marker.kwargs)

    yield fixture()

    fixture.set_last_failed(item.rep_call.failed)
