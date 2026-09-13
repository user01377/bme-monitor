# Administrating Devices

The `data-receiver` service provides several administrative scripts for managing registered devices and generating test data.

All scripts are located in the `scripts/` directory and **must be run from inside the `data-receiver` container**.

## Available Scripts

| Script                | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| `register_device`   | Registers a device and its public key               |
| `unregister_device` | Removes a registered device                         |
| `seed_test_device`  | Creates a test device for development and debugging |
| `gen-payload`       | Generates a test HTTP request payload               |

---

## Registering a Device

The `register_device` script registers a device in the service's SQLite database.

The script requires:

* A unique device name
* The device's public key in **hexadecimal format**

Run the script from inside the `data-receiver` container.

```bash
python -m scripts.register_device <name> <public_key>
```

The device's public key must be provided as a hexadecimal string.

### Example

```bash
python -m scripts.register_device esp32-01 a1b2c3d4...
```

Once registered, the device can authenticate with the `data-receiver` service using its corresponding private key.

---

## Unregistering a Device

The `unregister_device` script removes a registered device from the SQLite database.

The script requires:

* The name of the device to unregister

Run the script from inside the `data-receiver` container.

```bash
python -m scripts.unregister_device <name>
```

### Example

```bash
python -m scripts.unregister_device esp32-01
```

Unregistering a device removes its registration from the database. The device will no longer be able to authenticate with the `data-receiver` service.

---

## Seeding a Test Device

The `seed_test_device` script is intended **only for debugging and development**.

It creates a test device in the SQLite database and generates a corresponding key pair.

The script prints:

* Device name
* Private key
* Public key

Run the script from inside the `data-receiver` container.

```bash
python -m scripts.seed_test_device
```

The private key printed by this script should be treated as sensitive test data and should not be used as a production device key.

The generated private key can be used with the `gen-payload` script to generate authenticated test requests.

---

## Generating a Test Payload

The `gen-payload` script is intended **only for debugging and development**.

It generates an HTTP request that can be used for testing the `data-receiver` API through either:

* `curl`
* FastAPI Swagger UI

The script relies on a device created by `seed_test_device`.

**You do NOT need to run this script inside of the container.**

### Setup

1. Run the `seed_test_device` script.
2. Copy the **private key** printed by the `seed_test_device` script.
3. Paste the private key into the `gen-payload` script.
4. Run the `gen-payload` script.

```bash
python gen-payload
```

The generated request can then be copied and executed using `curl`, or its contents can be used to make a request through the FastAPI Swagger documentation.

> **Note:** `gen-payload` is intended for development and debugging only. It should not be used as part of the production device workflow.

---

## Script Requirements

All administrative scripts *(except for gen-payload)* must be executed **inside the `data-receiver` container**. They rely on the service's environment and SQLite database being available within the container.

For development and debugging:

```text
seed_test_device
       │
       ▼
  Test device
       │
       │ private key
       ▼
   gen-payload
       │
       ▼
 HTTP test request
```
