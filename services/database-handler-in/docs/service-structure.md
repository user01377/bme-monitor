# Service Structure

The `data-handler-in` service processes telemetry payloads from the Redis queue and is responsible for handling and storing incoming telemetry data in the main PostgreSQL database.

The service runs continuously, waiting for new payloads to become available in the Redis queue. When a payload is received, it is processed and inserted into the database.