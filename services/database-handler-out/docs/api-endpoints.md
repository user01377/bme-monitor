# API Structure

## `GET /telemetry`

Represents a generic telemetry data GET route for retrieving telemetry data from ESP32 nodes.

A device must be specified when querying telemetry. The `range` query parameter is optional and defaults to returning all readings from the past 24 hours.

### Query Parameters

| Parameter   | Type  | Required | Description                                                     |
| ----------- | ----- | -------- | --------------------------------------------------------------- |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query                                   |
| `metric`    | `str` | Yes      | Telemetry metric to retrieve: `temp`, `humidity`, or `pressure` |
| `range`     | `int` | No       | Number of hours of telemetry to retrieve. Defaults to `24`.     |

### Response Structure

Example JSON response:

```json
{
  "metric": "temp",
  "data": [
    {
      "timestamp": "2026-10-04T18:00:00Z",
      "value": 72.4
    },
    {
      "timestamp": "2026-10-04T18:10:00Z",
      "value": 72.6
    }
  ]
}
```

---

## `GET /telemetry/current`

Represents a telemetry data query for the most recent reading from an ESP32 node.

Returns the most recent temperature, humidity, and pressure readings from the specified device.

### Query Parameters

| Parameter   | Type  | Required | Description                   |
| ----------- | ----- | -------- | ----------------------------- |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query |

### Response Structure

Example JSON response:

```json
{
  "temperature": 72.4,
  "humidity": 48.2,
  "pressure": 1013.2
}
```

---

## `GET /nodes`

Represents diagnostic data for the ESP32 nodes.

### Query Parameters

| Parameter   | Type  | Required | Description                   |
| ----------- | ----- | -------- | ----------------------------- |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query |

### Response Structure

Example JSON response:

```json
{
  "data": [
    {
      "device": "esp32-01",
      "timestamp": "2026-10-04T18:00:00Z",
      "rssi": -48,
      "uptime": 86400,
      "reset": "power_on"
    }
  ]
}
```