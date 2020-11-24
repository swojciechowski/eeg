#include <DigiUSB.h>
#include <WS2811.h>

#define CTRL_BYTE      '\n'
#define DELAY           10
#define LED_NUM         1
#define LED_PIN         0

DEFINE_WS2811_FN(WS2811RGB, PORTB, LED_PIN)
RGB_t color[LED_NUM];

void setup() {
  pinMode(LED_PIN ,OUTPUT);
  DigiUSB.begin();
}

void loop() {
    /* Keep USB alive. Wait transmission delay.*/
    DigiUSB.delay(DELAY);

    if (DigiUSB.available() < 4) {
        return;
    }

    if (DigiUSB.read() == CTRL_BYTE) {
        DigiUSB.write(CTRL_BYTE);

        color[0].r = DigiUSB.read();
        color[0].g = DigiUSB.read();
        color[0].b = DigiUSB.read();
        WS2811RGB(color, ARRAYLEN(color));
    } else {
        DigiUSB.write(~CTRL_BYTE);
    }
}
