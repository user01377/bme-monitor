# API Structure

## `GET /api/telemetry`

Represents a generic telemetry data GET route for retrieving telemetry data from an ESP32 node.

A device must be specified when querying telemetry. The `range` query parameter is optional and defaults to returning readings from the past 24 hours.

The route supports retrieving a single telemetry metric: temperature, humidity, or pressure.

### Query Parameters

| Parameter     | Type    | Required | Description                                                          |
| ------------- | ------- | -------- | -------------------------------------------------------------------- |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query                                        |
| `metric`    | `str` | Yes      | Telemetry metric to retrieve:`temp`, `humidity`, or `pressure` |
| `range`     | `int` | No       | Number of hours of telemetry to retrieve. Defaults to`24`.         |

### Behavior

The route only returns readings belonging to the specified device and whose timestamps fall within the requested time range. Results are ordered chronologically from oldest to newest.

### Responses

**`200 OK`**

Example:

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

**`404 Not Found`**

Returned when the specified device does not exist:

```json
{
  "detail": "Device Not Found"
}
```

Returned when the device exists but has no readings within the requested time period:

```json
{
  "detail": "No Readings In Time Period"
}
```

**`422 Unprocessable Entity`**

Returned when a required parameter is missing or an invalid value is provided for `metric`.

---

## `GET /api/telemetry/current`

Represents a telemetry data query for the most recent reading from an ESP32 node.

Returns the most recent temperature, humidity, and pressure readings from the specified device.

### Query Parameters

| Parameter     | Type    | Required | Description                   |
| ------------- | ------- | -------- | ----------------------------- |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query |

### Behavior

The route retrieves the most recent telemetry reading for the specified device based on its timestamp.

### Responses

**`200 OK`**

Example:

```json
{
  "temperature": 72.4,
  "humidity": 48.2,
  "pressure": 1013.2
}
```

**`404 Not Found`**

Returned when the specified device does not exist.

```json
{
  "detail": "Device Not Found"
}
```

**`422 Unprocessable Entity`**

Returned when `device_id` is not provided.

---

## `GET /api/nodes`

Represents diagnostic data for ESP32 nodes.

The `device_id` parameter is optional. When omitted, the route returns the most recent diagnostic record for each device. When specified, it returns the most recent diagnostic record for that device.

### Query Parameters

| Parameter     | Type    | Required | Description                                                                               |
| ------------- | ------- | -------- | ----------------------------------------------------------------------------------------- |
| `device_id` | `str` | No       | ID of the ESP32 node to query. When omitted, diagnostic data for all devices is returned. |

### Behavior

The route returns the latest diagnostic record for each device, determined by the most recent timestamp.

When `device_id` is provided, only the latest diagnostic record for that device is returned.

### Responses

**`200 OK`**

Example:

```json
{
  "data": [
    {
      "device": "esp32-01",
      "timestamp": "2026-10-04T18:00:00Z",
      "rssi": -48,
      "uptime": 86400,
      "reset": "power_on"
    },
    {
      "device": "esp32-02",
      "timestamp": "2026-10-04T17:55:00Z",
      "rssi": -62,
      "uptime": 604800,
      "reset": "software"
    }
  ]
}
```

**`404 Not Found`**

When a `device_id` is provided but the device does not exist:

```json
{
  "detail": "Device Not Found"
}
```

**`422 Unprocessable Entity`**

Not applicable when `device_id` is omitted, since it is an optional parameter.
