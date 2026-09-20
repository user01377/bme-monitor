# Administrating Devices

The `data-receiver` service provides several administrative scripts for managing registered devices and generating test data.

All scripts are located in the `scripts/` directory and **must be run from inside the `data-receiver` container**.

## Available Scripts

| Script                | Purpose                                               |
| --------------------- | ----------------------------------------------------- |
| `list_devices`      | Lists all devices that are registered in the database |
| `register_device`   | Registers a device and its public key                 |
| `unregister_device` | Removes a registered device                           |
| `seed_test_device`  | Creates a test device for development and debugging   |
| `gen-payload`       | Generates a test HTTP request payload                 |

---

## Viewing All Registered Devices

The `list_devices` script prints out all devices which are registered inside of the service's SQLite database.

This script does not take any arguments.

Run the script from inside the `data-receiver` container.

```bash
python -m scripts.list_devices
```

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
