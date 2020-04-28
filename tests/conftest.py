import os
import tempfile

import pytest

from eshop import app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        yield client
