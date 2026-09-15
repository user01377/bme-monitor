#include <sodium.h>
#include "provision.h"
#include "device_storage.h"

void provisionDevice() {
    String deviceId;

    Serial.setTimeout(10000);

    Serial.println("\nHello! You have entered the provisioning step.");

    Serial.print("Enter the device ID to be set: ");

    while (Serial.available() == 0) {
        delay(10);
    }

    deviceId = Serial.readStringUntil('\n');
    deviceId.trim();

    if (deviceId.isEmpty()) {
        Serial.println("Invalid device ID.");
        return;
    }

    uint8_t publicKey[crypto_sign_PUBLICKEYBYTES];
    uint8_t privateKey[crypto_sign_SECRETKEYBYTES];

    Serial.println("\n\nGenerating secure Ed25519 key pair...");

    if (crypto_sign_keypair(publicKey, privateKey) != 0) {
        Serial.println("Failed to generate Ed25519 key pair.");
        return;
    }

    // save device id and private key to nvs
    saveDeviceId(deviceId);
    savePrivateKey(privateKey, crypto_sign_SECRETKEYBYTES);

    // Give public key to user
    Serial.println("Device provisioned.\n");
    
    Serial.println("Device ID: " + deviceId);

    Serial.print("Public Key (Hex): ");
    for(int i = 0; i < crypto_sign_PUBLICKEYBYTES; i++) {
        Serial.printf("%02x", publicKey[i]);
    }
    Serial.println("\n\n--- Setup Complete ---\n");

    setProvisioned(true);
}