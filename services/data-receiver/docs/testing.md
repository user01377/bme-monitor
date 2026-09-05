# Testing

Currently, this service contains one API route. Automated testing with PyTest has not yet been implemented. Instead, the service is currently tested through a combination of containerized integration testing and manual API requests.

Two test scripts are provided and must be executed in the following order.

## Test Procedure

1. **Build and run the containers**

   ```bash
   docker compose up --build
   ```

2. **Seed the local SQLite database**

   Run the provided database seed script from inside the appropriate container. This registers the test device and its public key.

3. **Configure the test client**

   Copy the test device's private key into `gen-payload.py`.

   > **Warning:** The private key is for testing purposes only and must not be committed to the repository.

4. **Generate a signed test payload**

   Run `gen-payload.py`. The script generates a payload containing:

   * Device ID
   * Timestamp
   * Base64-encoded sensor data
   * Ed25519 signature

5. **Send the payload to the API**

   Copy the generated `curl` command from the output of `gen-payload.py` and execute it, or use the generated payload through the FastAPI Swagger documentation.

6. **Verify the result**

   A successful request should return:

   ```json
   {
     "status": "queued"
   }
   ```

   The payload can then be inspected in Redis to verify that it was successfully added to `data_queue`.
