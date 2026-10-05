# Service Structure

> **Internal API**
>
> These endpoints are intended for internal communication between the `data-server` and `data-handler-out` service. They are not intended to be exposed directly to external clients.

The `data-handler-out` service is responsible for handling transactions between the database and the `data-server`. It acts as an internal middleman, allowing the `data-server` to request data without directly handling database queries and operations.

By offloading database-related work to this service, the `data-server` can focus on processing and serving data to its clients while `data-handler-out` handles retrieving the required information from the database.

This service is implemented using a **FastAPI** server.
