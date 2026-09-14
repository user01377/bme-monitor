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
2. The device's signature is valid.
3. The telemetry payload is valid.

If validation succeeds, the telemetry data is placed into the Redis queue for downstream processing.

The route does not directly interact with the PostgreSQL database.

---

## Device Authentication

The service maintains a local SQLite database containing information about registered ESP32 devices.

The database is used to determine whether a device is authorized to submit telemetry data.

Each registered device has a unique device ID and an associated Ed25519 public key. The corresponding private key is stored on the ESP32 node and is not transmitted to the `data-receiver` service.

When an ESP32 sends telemetry data, it creates a digital signature using its private key. The `data-receiver` retrieves the device's registered public key from SQLite and uses it to verify the signature.

### Signature Creation

The ESP32 creates a signature over the following data:

```text
device_id + timestamp + telemetry data
```

Telemetry values are represented as **scaled integers** before being serialized for a deterministic JSON representation. The receiver reconstructs the same representation when verifying the signature.

The signature therefore proves that:

* The request was created by a device possessing the registered private key.
* The signed telemetry data has not been modified after it was signed.

The private key never leaves the ESP32.

### Signature Verification

The authentication process is:

```text
ESP32
  │
  ├─ Collect telemetry data
  │
  ├─ Construct canonical message
  │
  ├─ Sign message with private key
  │
  └─ Send device ID + telemetry + signature
          │
          ▼
    data-receiver
          │
          ├─ Look up device ID in SQLite
          │
          ├─ Retrieve registered public key
          │
          ├─ Reconstruct canonical message
          │
          └─ Verify Ed25519 signature
                 │
          ┌──────┴──────┐
          │             │
        Valid         Invalid
          │             │
          ▼             ▼
        Redis          Reject
```

The exact serialization and signing implementation is maintained by the ESP32 and `data-receiver` code. Any changes to the signed message format must be made consistently on both sides to preserve signature verification.

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

1. An ESP32 node collects telemetry data.
2. The ESP32 constructs the canonical message from the device ID, timestamp, and telemetry data.
3. The ESP32 signs the message using its private Ed25519 key.
4. The ESP32 sends the telemetry data and signature to `data-receiver`.
5. `data-receiver` identifies the device from the request.
6. The device is looked up in the local SQLite database.
7. The device's registered public key is retrieved.
8. The signature is verified using the registered public key.
9. The telemetry payload is validated.
10. Authorized telemetry data is added to the Redis queue.
11. The request is returned to the ESP32.
12. A downstream service consumes the queued data.
13. The downstream service processes and stores the data in PostgreSQL.

This separation keeps the `data-receiver` service focused on **ingestion and authentication**, while database processing is handled independently.
