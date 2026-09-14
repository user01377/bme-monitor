# Administrating API Tokens

## General Information

The `scripts/` folder is copied into the data server container.

It contains two administrative scripts for managing API authentication tokens:

* `generate_api_token`
* `revoke_auth_token`

These scripts must be run from inside the data server container.

API token names must be unique. Attempting to create a token with an existing name will result in an error.

## Generate API Token

Use the following command inside the container shell:

```bash
python -m scripts.generate_api_token <name>
```

This will generate the new API token that can be handed out to a client.

**The generated API token is only printed once. Make sure to copy or write down the token and store it somewhere secure.**

Only the SHA-256 hash of the token is stored in the local SQLite database.

## Revoke API Token

Use the following command inside the container shell:

```bash
python -m scripts.revoke_auth_token <token_name>
```

Token revocation is based on the token's name.

Revoking a token prevents it from being used to authenticate with the data server. **This will not delete the token, it will be flagged as removed and will no longer be useable. This is for auditing.**

## Auditing

The SQLite database provides basic token usage auditing.

Each API token includes:

* `last_used_at` — Tracks the last time the token was successfully used.
* `revoked_at` — Tracks whether and when the token was revoked.
