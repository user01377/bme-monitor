#include <Preferences.h>
#include "device_storage.h"

Preferences device;

bool isProvisioned() {
    device.begin("identity", true);

    bool provisioned = device.getBool("provisioned", false);

    device.end();

    return provisioned;
}

void setProvisioned(bool flag) {
    device.begin("identity", false);

    device.putBool("provisioned", flag);

    device.end();
}

void saveDeviceId(const String& deviceId) {
    device.begin("identity", false);
    device.putString("device_id", deviceId);
    device.end();
}

String getDeviceId() {
    device.begin("identity", true);

    String deviceId = device.getString("device_id", "");

    device.end();

    return deviceId;
}

void savePrivateKey(const uint8_t* privateKey, size_t length) {
    device.begin("identity", false);

    device.putBytes("private_key", privateKey, length);

    device.end();
}

bool loadPrivateKey(uint8_t* privateKey, size_t length) {
    device.begin("identity", true);

    size_t storedLength = device.getBytesLength("private_key");

    if (storedLength != length) {
        device.end();
        return false;
    }

    size_t bytesRead = device.getBytes(
        "private_key",
        privateKey,
        length
    );

    device.end();

    return bytesRead == length;
}