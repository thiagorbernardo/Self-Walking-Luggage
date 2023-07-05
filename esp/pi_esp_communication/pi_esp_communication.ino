/*
 * There are three serial ports on the ESP known as U0UXD, U1UXD and U2UXD.
 * 
 * U0UXD is used to communicate with the ESP32 for programming and during reset/boot.
 * U1UXD is unused and can be used for your projects. Some boards use this port for SPI Flash access though
 * U2UXD is unused and can be used for your projects.
 * 
*/
#include <ArduinoJson.h>

#define RXD2 16  // ROXO
#define TXD2 17  // AZUl
#define START_CHAR '<'

void setup() {
  // Note the format for setting a serial port is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
  Serial.begin(115200);
  //Serial1.begin(9600, SERIAL_8N1, RXD2, TXD2);
  Serial2.begin(19200, SERIAL_8N1, RXD2, TXD2);
  Serial.println("Txd is on pin: " + String(TX));
  Serial.println("Rxd is on pin: " + String(RX));
  Serial.println("Baud Rate: " + String(Serial2.baudRate()));
}

void loop() {  //Choose Serial1 or Serial2 as required
  while (Serial2.available()) {
    // Read the incoming data
    char start = Serial2.read();  // read the start character
    //Serial.print("char ");
    //Serial.println(start);
    if (start == START_CHAR) {
      String data = Serial2.readStringUntil('\n');
      //Serial.println("Data received: " + data);

      // Parse the JSON data
      DynamicJsonDocument jsonDocument(1024);
      DeserializationError error = deserializeJson(jsonDocument, data);

      if (error) {
        // Serial.print("Failed to parse JSON data: ");
        // Serial.println(error.c_str());
      } else {
        // Get the values from the parsed JSON object
        float horizontal = jsonDocument["horizontal"];
        float distance = jsonDocument["distance"];

        // Do something with the values
        Serial.print("Horizontal:");
        Serial.print(horizontal);
        Serial.print(",");
        Serial.print("Distance:");
        Serial.println(distance);
      }
    }
  }
}