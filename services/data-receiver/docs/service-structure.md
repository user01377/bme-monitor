# Service Structure

## Overview

The `data-receiver` service is the entry point for ESP32 nodes that send telemetry data to the system.

Its primary responsibilities are:

1. Authenticate the device sending telemetry data.
2. Validate the received request.
3. Queue authorized telemetry data for downstream processing.

The service does **not** write telemetry data directly to PostgreSQL. Instead, authorized data is placed into a Redis queue and handled by a separate database handler service.

---

## Architecture

The general data flow is:

```text
ESP32 Node
    │
    │ HTTP request
    ▼
┌─────────────────────┐
│   data-receiver     │
│                     │
│  Device Validation  │
│         │           │
│         ▼           │
│   SQLite Database   │
└─────────┬───────────┘
          │
          │ Authorized telemetry
          ▼
    ┌───────────┐
    │   Redis   │
    │   Queue   │
    └─────┬─────┘
          │
          │ Queued telemetry
          ▼
  Database Handler
          │
          ▼
      PostgreSQL
```

---

## Responsibilities

The `data-receiver` service is responsible for:

* Receiving telemetry data from ESP32 nodes.
* Identifying the device sending the request.
* Authenticating the device using its registered credentials.
* Validating the received telemetry payload.
* Placing authorized telemetry data into the Redis queue.

The service is **not responsible for**:

* Storing telemetry data in PostgreSQL.
* Processing or aggregating telemetry data.
* Serving telemetry data to clients.
* Managing the application's public API.
* Performing administrative device management through HTTP endpoints.

---

## API

The service exposes a single API route for receiving telemetry data.

### `POST /queue-data`

This route is the entry point for telemetry data sent by ESP32 nodes.

The request is first validated to ensure that:

1. The device is registered.
2. The device is authorized to send data.
3. The telemetry payload is valid.

If validation succeeds, the telemetry data is placed into the Redis queue for downstream processing.

The route does not directly interact with PostgreSQL.

---

## Device Authentication

The service maintains a local SQLite database containing information about registered ESP32 devices.

The database is used to determine whether a device is authorized to submit telemetry data.

Each registered device contains the information required by the service to authenticate requests from that device.

Device registration and removal are handled through the administrative scripts located in the `scripts/` directory.

See [Administrating Devices](administrating-devices.md) for information about registering, unregistering, and testing devices.

---

## SQLite Database

The `data-receiver` service uses a local SQLite database for device authentication.

The SQLite database contains information about registered devices and their authentication credentials.

This database is separate from the PostgreSQL database used to store telemetry data.

### Purpose

SQLite is used for:

* Device registration
* Device authentication
* Device removal

Telemetry readings are **not** stored in this database.

---

## Redis Queue

After a telemetry request has been successfully authenticated and validated, the data is placed into a Redis queue.

Redis acts as the boundary between the `data-receiver` service and the downstream database-processing services.

This allows the receiver to accept telemetry data without needing to directly perform database operations.

The downstream database handler is responsible for consuming the queued data and storing it in PostgreSQL.

---

## Data Flow

A typical telemetry request follows this process:

1. An ESP32 node sends telemetry data to `data-receiver`.
2. `data-receiver` identifies the device from the request.
3. The device is looked up in the local SQLite database.
4. The device's credentials are validated.
5. The telemetry payload is validated.
6. Authorized telemetry data is added to the Redis queue.
7. The request is returned to the ESP32.
8. A downstream service consumes the queued data.
9. The downstream service processes and stores the data in PostgreSQL.

This separation keeps the `data-receiver` service focused on **ingestion and authentication**, while database processing is handled independently.
