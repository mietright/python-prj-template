import os
import pytest


LOCAL_DIR = os.path.dirname(__file__)


@pytest.fixture()
def docpath():
    return os.path.join(LOCAL_DIR, "data/test-1page.pdf")
