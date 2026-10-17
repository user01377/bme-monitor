import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_summary_valid(seeded_summary_db):
    response = client.get("/telemetry/summary")

    body = response.json()

    assert response.status_code == 200

    assert body["data"][0]["reading"] == "avg"
    assert body["data"][1]["reading"] == "high"
    assert body["data"][2]["reading"] == "low"

    # testing avg data w/ 0.1 delta
    assert body["data"][0]["temp"] == pytest.approx(23.3, abs=0.1)
    assert body["data"][0]["humidity"] == pytest.approx(46.6, abs=0.1)
    assert body["data"][0]["pressure"] == pytest.approx(1006.6, abs=0.1)

    # testing highest datapoint
    assert body["data"][1]["temp"] == 30
    assert body["data"][1]["humidity"] == 60
    assert body["data"][1]["pressure"] == 1020

    # testing lowest datapoint
    assert body["data"][2]["temp"] == 20
    assert body["data"][2]["humidity"] == 40
    assert body["data"][2]["pressure"] == 1000