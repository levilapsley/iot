#include <SPI.h>
#include <RH_RF95.h>

// LoRa module pins
#define RFM95_CS 10    
#define RFM95_RST 9    
#define RFM95_INT 2    

// LoRa frequency (915 MHz for Raspberry Pi script)
#define RF95_FREQ 915.0

// Initialize LoRa driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

// Integrated LED configuration
#define LED_PIN 13

void setup() {
  pinMode(LED_PIN, OUTPUT);          
  digitalWrite(LED_PIN, LOW);        


  // Reset LoRa module
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  // Initialize LoRa module
  if (!rf95.init()) {
    Serial.println("LoRa initialization failed.");
    while (1);                       // loop until initiliasation succeeds
  }

  // Set frequency to 915 MHz
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("Failed to set LoRa frequency.");
    while (1);
  }

  rf95.setTxPower(20, false);        // Radio power
  Serial.println("LoRa receiver ready at 915 MHz.");
}

void loop() {
  // Listen for incoming messages
  if (rf95.available()) {
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.recv(buf, &len)) {      // If a message is received
      digitalWrite(LED_PIN, HIGH);  // Turn on LED
      delay(50000);                   // Keep LED on for 50000ms
      digitalWrite(LED_PIN, LOW);   // Turn off LED

      Serial.println("Message received!");
    }
  }
}
