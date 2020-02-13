import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_database():
    pass  # add data to that remote database (start tests with different env vars)
    yield
    pass
