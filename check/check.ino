#include <FastLED.h>

#define RGB_PIN        	 9              // LED DATA PIN
#define RGB_LED_NUM    60            // 10 LEDs [0...9]
#define BRIGHTNESS       100           // brightness range [0..255]
#define CHIP_SET       WS2812B      // types of RGB LEDs
#define COLOR_CODE    GRB          //sequence of colors in data stream
// Define the array of LEDs
CRGB LEDs[RGB_LED_NUM];

// define 3 byte for the random color
#define UPDATES_PER_SECOND 10


void setup() {
  Serial.begin(9600);
  Serial.println("WS2812B LEDs strip Initialize");
  FastLED.addLeds<CHIP_SET, RGB_PIN, COLOR_CODE>(LEDs, RGB_LED_NUM);
  randomSeed(analogRead(0));
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 500);
  FastLED.clear();
  FastLED.show();
  for (int pin = 2; pin <= 7; pin++)
    pinMode(pin, INPUT);

}

void loop() {
    char buff[256];
    for (int pin = 0; pin <= 6; pin++) {
        if (digitalRead(pin + 2))
            LEDs[pin] = CRGB(0, 255, 0);
        else
            LEDs[pin] = CRGB(0, 0, 0);
    }
    FastLED.show();
}