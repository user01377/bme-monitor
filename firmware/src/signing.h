#ifndef SIGNING_H
#define SIGNING_H

#include <Arduino.h>

String signTelemetry(
    const String& deviceId,
    uint64_t timestamp,
    const String& dataJson
);

#endif