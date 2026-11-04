from datetime import date, timedelta

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    # Every test gets its own empty database file, so tests never touch real data.
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "DATABASE": str(tmp_path / "test.sqlite"),
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def tomorrow():
    return (date.today() + timedelta(days=1)).isoformat()


@pytest.fixture
def make_booking(client, tomorrow):
    """Post a booking. Any field can be overridden, e.g. make_booking(time="10:00")."""
    def _make(**overrides):
        form = {
            "customer_name": "Test Customer",
            "service": "Consultation",
            "date": tomorrow,
            "time": "09:00",
        }
        form.update(overrides)
        return client.post("/book", data=form)
    return _make
