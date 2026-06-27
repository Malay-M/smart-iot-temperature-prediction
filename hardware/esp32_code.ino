#include <WiFi.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <ThingSpeak.h>

// ==== Wi-Fi Credentials ====
char ssid[] = "YOUR_WIFI_SSID";     // your WiFi SSID
char pass[] = "YOUR_WIFI_PASSWORD";  // your WiFi password

// ==== ThingSpeak Credentials ====
unsigned long myChannelNumber = 0000000;    // Replace with your channel number
const char * myWriteAPIKey = "YOUR_WRITE_API_KEY";  // Replace with your Write API key

WiFiClient client;

// ==== Pin and Sensor Setup ====
#define DHTPIN 27
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

LiquidCrystal_I2C lcd(0x27, 16, 2);  // LCD I2C address

void setup() {
  Serial.begin(115200);

  // Initialize hardware
  dht.begin();
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");

  // Connect WiFi
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  lcd.setCursor(0, 0);
  lcd.print("WiFi Connected   ");

  // Initialize ThingSpeak
  ThingSpeak.begin(client);
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Sensor error");
    lcd.setCursor(0, 1);
    lcd.print("Sensor Error      ");
    delay(2000);
    return;
  }

  // Display on LCD
  lcd.setCursor(0, 1);
  lcd.print("T:");
  lcd.print(temp, 1);
  lcd.print((char)223);
  lcd.print("C H:");
  lcd.print(hum, 1);
  lcd.print("% ");

  // Print to Serial
  Serial.print("T: ");
  Serial.print(temp);
  Serial.print(" C, H: ");
  Serial.print(hum);
  Serial.println(" %");

  // ==== Send to ThingSpeak ====
  ThingSpeak.setField(1, temp);  // Field1 = Temperature
  ThingSpeak.setField(2, hum);   // Field2 = Humidity

  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
  if (x == 200) {
    Serial.println("Channel update successful.");
  } else {
    Serial.println("Problem updating channel. HTTP error code " + String(x));
  }

  delay(20000); // ThingSpeak allows update every 15 seconds minimum
}
