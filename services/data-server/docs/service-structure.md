# Data Server Service Structure

## General Information

The data server is the client-facing entrypoint for the telemetry server.

Every request to the data server requires a valid API authentication token. All routes are protected by an authentication check.

The authentication logic is implemented in the `authenticate_user` function inside `routes.py`.

### Local Database

This service contains a local SQLite database.

The SQLite database is used only for:

* API token storage
* User authentication

The database is local to the data server container and is not shared with the main PostgreSQL database.

## Data Modeling

### `api_tokens`

The `api_tokens` table stores authentication tokens used by clients to access the data server.

API tokens are stored as hashes rather than plaintext tokens.

| Column         | Type        | Constraints               | Description                       |
| -------------- | ----------- | ------------------------- | --------------------------------- |
| `id`           | Integer     | Primary key               | Unique identifier for the token   |
| `token_hash`   | String(64)  | Unique, Not Null, Indexed | SHA-256 hash of the API token     |
| `name`         | String(100) | Unique, Not Null          | Unique name identifying the token |
| `created_at`   | DateTime    | Not Null                  | Time the token was created        |
| `last_used_at` | DateTime    | Nullable                  | Time the token was last used      |
| `revoked_at`   | DateTime    | Nullable                  | Time the token was revoked        |

A token is considered valid when it exists, has not been revoked, and matches the hash of the API token provided by the client.
