#include <Arduino.h>

#ifdef PROVISIONING

#include <provision.h>

void setup() {
    Serial.begin(115200);
    delay(1000);

    provisionDevice();
}

void loop() {
}

#else

#include <Adafruit_BME280.h>
#include <WiFi.h>
#include <time.h>
#include <HTTPClient.h>
#include <signing.h>
#include <device_storage.h>
#include <secrets.h>

Adafruit_BME280 bme;

const unsigned long POLL_INTERVAL_MINUTES = 10;
const unsigned long POLL_INTERVAL_MS = POLL_INTERVAL_MINUTES * 60UL * 1000UL;

bool syncTime() {
    configTime(0, 0, NTP_SERVER);

    time_t now = time(nullptr);

    int attempts = 0;
    while (now < 100000 && attempts < 20) {
        delay(500);
        now = time(nullptr);
        attempts++;
    }

    if (now < 100000) {
        Serial.println("Failed to synchronize time.");
        return false;
    }

    Serial.println("Time synchronized.");
    return true;
}

void setup() {
    Serial.begin(115200);

    delay(2000);

    Serial.println("BOOTING");

    if (!isProvisioned()) {
        Serial.println("Device is not provisioned.");
        
        while (true) {
            delay(1000);
        }
    }

    if (!bme.begin(0x76)) {
        while (true) {
            delay(1000);
        }
    }

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);


    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    while (!syncTime()) {
        delay(1000);
    }
}

void loop() {
    int32_t scaledTemp = round(bme.readTemperature() * 100);
    int32_t scaledHumidity = round(bme.readHumidity() * 100);
    int32_t scaledPressure = round((bme.readPressure() / 100.0F) * 100);
    int64_t timestamp = time(nullptr);

    String signData =
        "{\"humidity\":" + String(scaledHumidity) +
        ",\"pressure\":" + String(scaledPressure) +
        ",\"temperature\":" + String(scaledTemp) +
        "}";

    // debug statement for visualizing data
    // Serial.println(signData);

    String deviceId = getDeviceId();
    String signature = signTelemetry(deviceId, timestamp, signData);

    if (WiFi.status() == WL_CONNECTED) {

        HTTPClient http;

        http.begin(API_URL);
        http.addHeader("Content-Type", "application/json");

        String data_json = "{";
        data_json += "\"device_id\":\"" + deviceId + "\",";
        data_json += "\"timestamp\":" + String(timestamp) + ",";
        data_json += "\"data\":{";
        data_json += "\"temperature\":" + String(scaledTemp) + ",";
        data_json += "\"humidity\":" + String(scaledHumidity) + ",";
        data_json += "\"pressure\":" + String(scaledPressure);
        data_json += "},";
        data_json += "\"signature\":\"";
        data_json += signature;
        data_json += "\"";
        data_json += "}";

        int response_code = http.POST(data_json);

        // debugging for http response
        // Serial.print("HTTP response: ");
        // Serial.println(response_code);

        if (response_code > 0) {
            Serial.println(http.getString());
        } else {
            Serial.println(http.errorToString(response_code));
        }

        http.end();
    }

    // Serial.println(scaledTemp);
    // Serial.println(scaledHumidity);
    // Serial.println(scaledPressure);
    // Serial.println(WiFi.localIP());

    delay(POLL_INTERVAL_MS);
}

#endif