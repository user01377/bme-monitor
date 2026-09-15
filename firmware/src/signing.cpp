#include "signing.h"
#include "device_storage.h"

#include <sodium.h>

String signTelemetry(const String& deviceId, uint64_t timestamp, const String& dataJson) {
    /**
    * This is a helper function for main which constructs the signature exactly how the API expects.
    */

    uint8_t privateKey[crypto_sign_SECRETKEYBYTES];

    if (!loadPrivateKey(privateKey, sizeof(privateKey))) {
        return "";
    }

    size_t messageLength =
        deviceId.length() +
        sizeof(timestamp) +
        dataJson.length();

    uint8_t* message = new uint8_t[messageLength];

    size_t offset = 0;

    memcpy(
        message + offset,
        deviceId.c_str(),
        deviceId.length()
    );
    offset += deviceId.length();

    for (int i = 7; i >= 0; i--) {
        message[offset++] = (timestamp >> (i * 8)) & 0xFF;
    }

    memcpy(
        message + offset,
        dataJson.c_str(),
        dataJson.length()
    );

    uint8_t signature[crypto_sign_BYTES];
    unsigned long long signatureLength;

    if (crypto_sign_detached(
        signature,
        &signatureLength,
        message,
        messageLength,
        privateKey
    ) != 0) {
        delete[] message;
        return "";
    }

    delete[] message;

    char encoded[sodium_base64_ENCODED_LEN(
        crypto_sign_BYTES,
        sodium_base64_VARIANT_ORIGINAL
    )];
    
    sodium_bin2base64(
        encoded,
        sizeof(encoded),
        signature,
        signatureLength,
        sodium_base64_VARIANT_ORIGINAL
    );

    return String(encoded);
}