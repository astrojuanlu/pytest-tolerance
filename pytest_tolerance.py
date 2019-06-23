import pytest


@pytest.fixture
def tolerance(request):
    return 1e-6
