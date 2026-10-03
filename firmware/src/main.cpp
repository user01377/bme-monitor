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
#include <ArduinoJson.h>

Adafruit_BME280 bme;

const unsigned long POLL_INTERVAL_MINUTES = 10;
const unsigned long POLL_INTERVAL_MS = POLL_INTERVAL_MINUTES * 60UL * 1000UL;
String resetReason;

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

void connectWifi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    while (!syncTime()) {
        delay(1000);
    }
}

String getResetReason() {
    // simplifies the reset reason from what esp_reset_reason returns
    
    switch (esp_reset_reason()) {
        case ESP_RST_POWERON:
            return "power_on";

        case ESP_RST_PANIC:
            return "panic";

        case ESP_RST_INT_WDT:
        case ESP_RST_TASK_WDT:
        case ESP_RST_WDT:
            return "watchdog";

        case ESP_RST_BROWNOUT:
            return "brownout";

        case ESP_RST_SW:
            return "software";

        case ESP_RST_EXT:
            return "external";

        case ESP_RST_DEEPSLEEP:
            return "deep_sleep";

        case ESP_RST_SDIO:
            return "sdio";

        default:
            return "unknown";
    }
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

    connectWifi();

    resetReason = getResetReason();
}

void loop() {
    // RETRY CONNECTON TO WIFI IF CONNECTION IS LOST
    if (WiFi.status() != WL_CONNECTED) {
        WiFi.reconnect();

        int wifi_attempts = 0;

        while (WiFi.status() != WL_CONNECTED && wifi_attempts < 10) {
            delay(500);
            wifi_attempts++;
        }

        // SYNC TIME WITH NTP SERVER
        syncTime();

        return;
    }

    if (WiFi.status() == WL_CONNECTED) {
        // TELEMETRY DATA
        int32_t scaledTemp = round(bme.readTemperature() * 100);
        int32_t scaledHumidity = round(bme.readHumidity() * 100);
        int32_t scaledPressure = round((bme.readPressure() / 100.0F) * 100);

        String deviceId = getDeviceId();

        HTTPClient http;

        http.begin(API_URL);
        http.addHeader("Content-Type", "application/json");
        http.setUserAgent("ESP32-(" + deviceId + ")");
    
        JsonDocument jsondoc;

        int64_t timestamp = time(nullptr);

        // ADD AUTH DATA
        jsondoc["device_id"] = deviceId;
        jsondoc["timestamp"] = timestamp;

        // ADD TELEMETRY DATA
        JsonObject dataJsonObject = jsondoc["data"].to<JsonObject>();
        dataJsonObject["humidity"] = scaledHumidity;
        dataJsonObject["pressure"] = scaledPressure;
        dataJsonObject["temperature"] = scaledTemp;

        // SERALIZE TELEMETRY DATA TO CREATE SIGNATURE
        String dataJson;
        serializeJson(dataJsonObject, dataJson);
        String signature = signTelemetry(deviceId, timestamp, dataJson);

        // ADD SIGNATURE
        jsondoc["signature"] = signature;

        int16_t rssi = WiFi.RSSI();
        uint32_t uptime = millis() / 1000; // if node persists for more than 49.7 days, uptime will reset

        JsonObject diagnosticJsonObject = jsondoc["diagnostics"].to<JsonObject>();
        diagnosticJsonObject["rssi"] = rssi;
        diagnosticJsonObject["uptime"] = uptime;
        diagnosticJsonObject["reset"] = resetReason;

        // SERIALIZE JSONDOC TO DATA_JSON VARIABLE
        String data_json;
        serializeJson(jsondoc, data_json);

        // DEBUG STATEMENT FOR DATA_JSON
        // Serial.println(data_json);

        int response_code = http.POST(data_json);

        // DEBUG FOR HTTP RESPONSE
        // Serial.print("HTTP response: ");
        // Serial.println(response_code);

        if (response_code > 0) {
            Serial.println(http.getString());
        } else {
            Serial.println(http.errorToString(response_code));
        }

        http.end();
    } else {
        return;
    }

    delay(POLL_INTERVAL_MS);
}

#endif