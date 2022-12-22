#include <SPI.h>
#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

#include "arduino_secrets.h"

int readAmounts;
int seconds;
int soundPin;
int motionPin;
int soundVal;
int motionVal;

char ssid[] = SECRET_SSID;    // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int status = WL_IDLE_STATUS;  // the WiFi radio's status

char serverAddress[] = "232c-70-81-224-189.ngrok.io";

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress);

void setup() {
  Serial.begin(9600);  // setup serial

  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true)
      ;
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the data:
  Serial.print("You're connected to the network");
  printCurrentNet();
  printWifiData();

  readAmounts = 0;
  seconds = 60;
  soundPin = A0;
  motionPin = 5;
  soundVal = 0;
  motionVal = 0;
}


void loop() {
  readAmounts++;
  int soundRead = analogRead(soundPin);
  int motionRead = digitalRead(motionPin);

  if (motionRead) {
    motionVal++;
  }

  soundVal += soundRead;

  if (readAmounts == seconds) {
    Serial.println("making sound request");

    DynamicJsonDocument soundDoc(1024);

    int soundAvg = soundVal / seconds;

    soundDoc["value"] = soundAvg;
    soundDoc["sensorId"] = "ClementSoundSensor";

    String soundPostData;

    serializeJson(soundDoc, soundPostData);

    client.beginRequest();
    client.post("/api/sound");
    client.sendHeader("Content-Type", "application/json");
    client.sendHeader("Content-Length", soundPostData.length());
    client.beginBody();
    client.print(soundPostData);
    client.println();
    client.endRequest();

    // read the status code and body of the response
    int soundStatusCode = client.responseStatusCode();
    String soundResponse = client.responseBody();

    Serial.print("Status code: ");
    Serial.println(soundStatusCode);
    Serial.print("Response: ");
    Serial.println(soundResponse);

    Serial.println("making motion request");

    DynamicJsonDocument motionDoc(1024);

    motionDoc["value"] = motionVal;
    motionDoc["sensorId"] = "ClementMotionSensor";

    String motionPostData;

    serializeJson(motionDoc, motionPostData);

    client.beginRequest();
    client.post("/api/motion");
    client.sendHeader("Content-Type", "application/json");
    client.sendHeader("Content-Length", motionPostData.length());
    client.beginBody();
    client.print(motionPostData);
    client.println();
    client.endRequest();

    // read the status code and body of the response
    int motionStatusCode = client.responseStatusCode();
    String motionResponse = client.responseBody();

    Serial.print("Status code: ");
    Serial.println(motionStatusCode);
    Serial.print("Response: ");
    Serial.println(motionResponse);

    soundVal = 0;
    motionVal = 0;
    readAmounts = 0;
  }

  delay(1000);
}

void printWifiData() {
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  Serial.println(ip);

  // print your MAC address:
  byte mac[6];
  WiFi.macAddress(mac);
  Serial.print("MAC address: ");
  printMacAddress(mac);
}

void printCurrentNet() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the MAC address of the router you're attached to:
  byte bssid[6];
  WiFi.BSSID(bssid);
  Serial.print("BSSID: ");
  printMacAddress(bssid);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

  // print the encryption type:
  byte encryption = WiFi.encryptionType();
  Serial.print("Encryption Type:");
  Serial.println(encryption, HEX);
  Serial.println();
}

void printMacAddress(byte mac[]) {
  for (int i = 5; i >= 0; i--) {
    if (mac[i] < 16) {
      Serial.print("0");
    }
    Serial.print(mac[i], HEX);
    if (i > 0) {
      Serial.print(":");
    }
  }
  Serial.println();
}