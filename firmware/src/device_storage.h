#ifndef DEVICE_STORAGE_H
#define DEVICE_STORAGE_H

#include <Arduino.h>

bool isProvisioned();

void setProvisioned(bool flag);

void saveDeviceId(const String& deviceId);

String getDeviceId();

void savePrivateKey(const uint8_t* privateKey, size_t length);

bool loadPrivateKey(uint8_t* privateKey, size_t length);

#endif