# API Structure

The `data-server` API provides telemetry readings, node diagnostics, daily summaries, and recent trends from ESP32 sensor nodes.

## Overview of Endpoints

| Method  | Endpoint                   | Description                                                     |
| ------- | -------------------------- | --------------------------------------------------------------- |
| `GET` | `/api/telemetry`         | Retrieve one metric for one device over a requested time range. |
| `GET` | `/api/telemetry/current` | Retrieve the latest reading for one device.                     |
| `GET` | `/api/nodes`             | Retrieve node diagnostics and today's reading counts.           |
| `GET` | `/api/telemetry/summary` | Retrieve today's averages, highs, and lows across all devices.  |
| `GET` | `/api/telemetry/trend`   | Retrieve per-device trends relative to recent averages.         |

## Data Conventions

- Temperature is measured in degrees Fahrenheit (°F).
- Humidity is measured as relative humidity (%).
- Pressure is measured in hectopascals (hPa).
- Timestamps are ISO 8601 datetimes. Examples use UTC (`Z`).
- “Today” means the current calendar day in `America/New_York`, from midnight inclusive to the next midnight exclusive.
- Device existence is determined by the presence of telemetry records for that device.

Error responses use a `detail` field. For example:

```json
{
  "detail": "Device Not Found"
}
```

---

## `GET /api/telemetry`

Returns a time series for a single metric from a specified ESP32 node.

### Query Parameters

| Parameter     | Type    | Required | Description                                                 |
| ------------- | ------- | -------- | ----------------------------------------------------------- |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query.                              |
| `metric`    | `str` | Yes      | Metric to retrieve:`temp`, `humidity`, or `pressure`. |
| `range`     | `int` | No       | Number of hours to look back. Defaults to`24`.            |

### Behavior

Returns readings for the specified device with timestamps at or after the current time minus `range` hours. Results are ordered chronologically, from oldest to newest. Each point contains a timestamp and the selected metric's value.

### Example Request

```http
GET /api/telemetry?device_id=vn-001&metric=temp&range=24
```

### Responses

**`200 OK`**

```json
{
  "metric": "temp",
  "data": [
    {
      "timestamp": "2026-10-11T18:00:00Z",
      "value": 72.4
    },
    {
      "timestamp": "2026-10-11T18:10:00Z",
      "value": 72.6
    }
  ]
}
```

**`404 Not Found`**

| Detail                         | Condition                                                           |
| ------------------------------ | ------------------------------------------------------------------- |
| `Device Not Found`           | The specified device has no telemetry records.                      |
| `No Readings In Time Period` | The device exists but has no readings in the requested time window. |

**`422 Unprocessable Entity`**

Returned when a required parameter is missing, `metric` is not supported, or `range` cannot be parsed as an integer.

---

## `GET /api/telemetry/current`

Returns the most recent temperature, humidity, pressure, and timestamp for a specified ESP32 node.

### Query Parameters

| Parameter     | Type    | Required | Description                    |
| ------------- | ------- | -------- | ------------------------------ |
| `device_id` | `str` | Yes      | ID of the ESP32 node to query. |

### Behavior

Returns the device's latest telemetry record based on its timestamp. No time window is applied: if a node stops reporting, its last recorded reading is still returned. Clients can use `timestamp` to determine the reading's age.

### Example Request

```http
GET /api/telemetry/current?device_id=vn-001
```

### Responses

**`200 OK`**

```json
{
  "temperature": 72.6,
  "humidity": 48.2,
  "pressure": 1013.2,
  "timestamp": "2026-10-11T18:10:00Z"
}
```

**`404 Not Found`**

| Detail                | Condition                                                                 |
| --------------------- | ------------------------------------------------------------------------- |
| `Device Not Found`  | The specified device has no telemetry records during device verification. |
| `No Readings Found` | No record is available when retrieving the latest reading.                |

**`422 Unprocessable Entity`**

Returned when `device_id` is missing.

---

## `GET /api/nodes`

Returns the latest diagnostic record for each node, including its telemetry reading count for today.

### Query Parameters

| Parameter     | Type    | Required | Description                                                                          |
| ------------- | ------- | -------- | ------------------------------------------------------------------------------------ |
| `device_id` | `str` | No       | ID of the ESP32 node to query. Omit to retrieve all devices with diagnostic records. |

### Behavior

Returns the most recent diagnostic record for each matching device. Diagnostic records can be older than today. The `readings` field counts telemetry records within today's calendar-day boundaries and defaults to `0` if none exist.

The response always contains a `data` array, even when querying one device. Devices without diagnostic records are omitted; no matching diagnostic records returns an empty array with `200 OK`.

### Response Fields

| Field         | Description                                   |
| ------------- | --------------------------------------------- |
| `device`    | Device ID.                                    |
| `readings`  | Number of telemetry readings recorded today.  |
| `timestamp` | Timestamp of the latest diagnostic record.    |
| `rssi`      | Device-reported Wi-Fi signal strength in dBm. |
| `uptime`    | Device-reported uptime in seconds.            |
| `reset`     | Device-reported reset reason.                 |

### Example Requests

```http
GET /api/nodes
GET /api/nodes?device_id=vn-001
```

### Responses

**`200 OK`**

```json
{
  "data": [
    {
      "device": "jw-001",
      "readings": 84,
      "timestamp": "2026-10-11T18:00:00Z",
      "rssi": -62,
      "uptime": 604800,
      "reset": "software"
    },
    {
      "device": "vn-001",
      "readings": 85,
      "timestamp": "2026-10-11T18:10:00Z",
      "rssi": -48,
      "uptime": 86400,
      "reset": "power_on"
    }
  ]
}
```

When no diagnostic records match:

```json
{
  "data": []
}
```

**`404 Not Found`**

Returned with `detail: "Device Not Found"` when a device is specified but has no telemetry records, even if diagnostic records exist.

Omitting the optional `device_id` does not produce a missing-parameter validation error.

---

## `GET /api/telemetry/summary`

Returns today's average, highest, and lowest temperature, humidity, and pressure across all devices.

### Query Parameters

None. Device, metric, and time-range filters are not supported.

### Behavior

Calculates each metric's average, maximum, and minimum across all telemetry readings recorded today. The response contains three entries in order: `avg`, `high`, and `low`.

Averages are calculated across individual readings, so devices with more readings contribute more to the average. Each metric's high or low may come from a different device or reading.

### Example Request

```http
GET /api/telemetry/summary
```

### Responses

**`200 OK`**

```json
{
  "data": [
    {
      "reading": "avg",
      "temp": 72.4,
      "humidity": 48.2,
      "pressure": 1013.2
    },
    {
      "reading": "high",
      "temp": 75.1,
      "humidity": 53.6,
      "pressure": 1015.4
    },
    {
      "reading": "low",
      "temp": 69.8,
      "humidity": 43.9,
      "pressure": 1010.7
    }
  ]
}
```

**`404 Not Found`**

Returned when no telemetry readings exist today:

```json
{
  "detail": "No Readings Today"
}
```

---

## `GET /api/telemetry/trend`

Returns trend directions for each device by comparing its latest temperature, humidity, and pressure with its averages over the past three hours.

### Query Parameters

| Parameter     | Type    | Required | Description                                                                                         |
| ------------- | ------- | -------- | --------------------------------------------------------------------------------------------------- |
| `device_id` | `str` | No       | ID of the ESP32 node to query. Omit to retrieve all devices with readings in the comparison window. |

### Behavior

Calculates a separate three-hour average for each device and metric, then compares the device's latest value with that average. The comparison period is configured by `COMPARE_PAST_HOURS` in the backend and cannot be changed through a query parameter.

| Comparison                               | Trend enum member |
| ---------------------------------------- | ----------------- |
| Latest value is greater than the average | `UP`            |
| Latest value is less than the average    | `DOWN`          |
| Latest value equals the average          | `NEUTRAL`       |

The latest reading contributes to the average when it falls within the comparison window. A device with only one reading in that window therefore returns neutral trends. Comparisons use exact values without a tolerance.

Devices with no readings in the comparison window are omitted. An existing device with no recent readings returns an empty `data` array with `200 OK`.

### Example Requests

```http
GET /api/telemetry/trend
GET /api/telemetry/trend?device_id=vn-001
```

### Responses

**`200 OK`**

Returns a `data` array containing one object per matching device:

| Field        | Description                                      |
| ------------ | ------------------------------------------------ |
| `device`   | Device ID.                                       |
| `temp`     | Temperature trend, serialized from`TrendEnum`. |
| `humidity` | Humidity trend, serialized from`TrendEnum`.    |
| `pressure` | Pressure trend, serialized from`TrendEnum`.    |

The exact JSON trend values are defined by `TrendEnum` in `schema.py`; enum member names above describe the comparison logic. The response does not include numeric averages, differences, or timestamps.

When no readings match:

```json
{
  "data": []
}
```

**`404 Not Found`**

Returned when a device is specified but has no telemetry records:

```json
{
  "detail": "Device Not Found"
}
```

Omitting the optional `device_id` does not produce a missing-parameter validation error.
