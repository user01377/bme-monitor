# API Structure

> **Internal API**
>
> These endpoints are used by `data-server` to retrieve data from `database-handler-out`. They are not intended to be exposed directly to external clients.

Temperature is measured in °F, humidity in %, and pressure in hPa. Daily calculations use the `America/New_York` timezone. Paths are relative to any configured router prefix.

## `GET /telemetry`

Returns one metric for a specified device over the requested time range, ordered from oldest to newest.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `device_id` | `str` | Yes | Device ID. |
| `metric` | `str` | Yes | `temp`, `humidity`, or `pressure`. |
| `range` | `int` | No | Hours to look back. Defaults to `24`. |

**Response — `200 OK`**

```json
{
  "metric": "temp",
  "data": [
    { "timestamp": "2026-10-11T18:00:00Z", "value": 72.4 },
    { "timestamp": "2026-10-11T18:10:00Z", "value": 72.6 }
  ]
}
```

**Errors:**

- `404`: `Device Not Found` or `No Readings In Time Period`.
- `422`: Missing required parameters, unsupported metric, or a non-integer range.

## `GET /telemetry/current`

Returns the most recent temperature, humidity, pressure, and timestamp for a specified device.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `device_id` | `str` | Yes | Device ID. |

**Response — `200 OK`**

```json
{
  "temperature": 72.6,
  "humidity": 48.2,
  "pressure": 1013.2,
  "timestamp": "2026-10-11T18:10:00Z"
}
```

**Errors:**

- `404`: `Device Not Found` or `No Readings Found`.
- `422`: Missing `device_id`.

## `GET /nodes`

Returns the latest diagnostic record for each device and its telemetry reading count for today. Specify `device_id` to retrieve one device.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `device_id` | `str` | No | Device ID. Omit to retrieve all devices with diagnostic records. |

**Response — `200 OK`**

```json
{
  "data": [
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

`rssi` is measured in dBm and `uptime` in seconds. `readings` defaults to `0` when the device has no telemetry readings today. No matching diagnostics returns `200 OK` with an empty `data` array.

**Errors:**

- `404`: `Device Not Found` when the specified device has no telemetry records.

## `GET /telemetry/summary`

Returns today's averages, highs, and lows across telemetry readings from all devices. No query parameters are required or supported.

**Response — `200 OK`**

```json
{
  "data": [
    { "reading": "avg", "temp": 72.4, "humidity": 48.2, "pressure": 1013.2 },
    { "reading": "high", "temp": 75.1, "humidity": 53.6, "pressure": 1015.4 },
    { "reading": "low", "temp": 69.8, "humidity": 43.9, "pressure": 1010.7 }
  ]
}
```

**Errors:**

- `404`: `No Readings Today` when no telemetry readings exist today.

## `GET /telemetry/trend`

Compares each device's latest temperature, humidity, and pressure with its averages over the past three hours, configured by `COMPARE_PAST_HOURS`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `device_id` | `str` | No | Device ID. Omit to retrieve all devices with recent readings. |

**Response — `200 OK`**

Returns a `data` array containing `device`, `temp`, `humidity`, and `pressure`. Each metric contains a trend value defined by `TrendEnum`:

| Comparison | Enum member |
| --- | --- |
| Latest value above average | `UP` |
| Latest value below average | `DOWN` |
| Latest value equal to average | `NEUTRAL` |

The exact serialized values are defined in `schema.py`. Devices without readings in the comparison window are omitted. No matching readings returns `200 OK` with an empty `data` array.

**Errors:**

- `404`: `Device Not Found` when the specified device has no telemetry records.
