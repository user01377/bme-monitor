from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_get_telemetry_temp(seeded_db):
    response = client.get("/telemetry", params={"device_id": "test-device", "metric": "temp"})

    assert response.status_code == 200

    body = response.json()

    assert body["metric"] == "temp"
    assert len(body["data"]) == 3
    assert [point["value"] for point in body["data"]] == [30, 20, 20]

def test_get_telemetry_humidity(seeded_db):
    response = client.get(
        "/telemetry",
        params={"device_id": "test-device", "metric": "humidity"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["metric"] == "humidity"
    assert len(body["data"]) == 3
    assert [point["value"] for point in body["data"]] == [60, 40, 40]


def test_get_telemetry_pressure(seeded_db):
    response = client.get(
        "/telemetry",
        params={"device_id": "test-device", "metric": "pressure"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["metric"] == "pressure"
    assert len(body["data"]) == 3
    assert [point["value"] for point in body["data"]] == [1020, 1000, 1000]


def test_get_telemetry_ordered_by_timestamp(seeded_db):
    response = client.get(
        "/telemetry",
        params={"device_id": "test-device", "metric": "temp"},
    )

    assert response.status_code == 200

    timestamps = [
        point["timestamp"]
        for point in response.json()["data"]
    ]

    assert timestamps == sorted(timestamps)


def test_get_telemetry_metric_returned(seeded_db):
    for metric in ["temp", "humidity", "pressure"]:
        response = client.get(
            "/telemetry",
            params={"device_id": "test-device", "metric": metric},
        )

        assert response.status_code == 200
        assert response.json()["metric"] == metric

def test_get_telemetry_invalid_metric(seeded_db):
    response = client.get(
        "/telemetry",
        params={"device_id": "test-device", "metric": "invalid"},
    )

    assert response.status_code == 422

def test_get_telemetry_missing_device_id(seeded_db):
    response = client.get(
        "/telemetry",
        params={"metric": "temp"},
    )

    assert response.status_code == 422

def test_get_telemetry_invalid_device(seeded_db):
    response = client.get(
        "/telemetry",
        params={"device_id": "other-device", "metric": "temp"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Device Not Found"

def test_get_telemetry_invalid_range(seeded_db):
    response = client.get(
        "/telemetry",
        params={"device_id": "test-device", "metric": "temp", "range": 1},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "No Readings In Time Period"
