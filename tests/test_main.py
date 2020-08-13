"""
Create falcon client to test API
"""
from pathlib import Path

import pytest
from falcon import testing

from project.app import app


@pytest.fixture()
def client():
    """
    use app to create a Falcon TestClient
    """
    return testing.TestClient(app)


def test_settings_on_get(client):
    """
    test_settings_on_get
    """
    result = client.simulate_get("/settings")
    if __debug__:
        if result.status_code != 200 or result.text != "ok":
            raise AssertionError("test_settings_on_get error!")


def test_settings_on_post(client):
    """
    test_settings_on_get
    """
    json_payload = {"payload": {"test": None}, "filepath": "./tests"}
    result = client.simulate_post("/settings", json=json_payload)
    if __debug__:
        if result.status_code != 201 or not Path(json_payload["filepath"]).exists():
            raise AssertionError("test_settings_on_post error!")
