/*
 * PicoTemp
 *
 *
 * Authors: Sebastian Garcia
 *          Juan Sebastian Guerrero
 *          Juliana Lucia Pineda
 *          Laura Sofia Valero
 *
 */

// Timer Interrupt
#define TIMER_INTERRUPT_DEBUG 0
#define _TIMERINTERRUPT_LOGLEVEL_ 0
#include "RPi_Pico_TimerInterrupt.h"
RPI_PICO_Timer ITimer0(0);
#define READ_INTERVAL_MS 3000  // How often to read the temperature (recommended greater than 2000)

// Pin definitions
#define LED_PIN 25
#define ANALOG_PIN 28
#define CALIBRATION_0_PIN 22
#define CALIBRATION_100_PIN 21

// ADC Definitions
#define NUM_SAMPLES 100
#define READ_DELAY_MS 2

// PT100 Calibration
#define PT100_SLOPE 2.730021
#define PT100_INTERCEPT -284.474438

// CIRCUIT Calibration
#define RESISTOR_0 100.7
#define RESISTOR_100 137.7
#define CIRCUIT_SLOPE_DEFAULT 0.04  // Default values
#define CIRCUIT_INTERCEPT_DEFAULT 99.55
float circuit_slope = CIRCUIT_SLOPE_DEFAULT;
float circuit_intercept = CIRCUIT_INTERCEPT_DEFAULT;

bool calibrating = false;

void setup() {
    // Pin definitions
    pinMode(LED_PIN, OUTPUT);
    pinMode(CALIBRATION_0_PIN, INPUT_PULLUP);
    pinMode(CALIBRATION_100_PIN, INPUT_PULLUP);

    // Disable power-saving mode (See page 17 on datasheet)
    pinMode(23, OUTPUT);
    digitalWrite(23, HIGH);

    // Serial communication
    Serial.begin(115200);
    while (!Serial)
        ;
    delay(100);

    // Calibration
    // TODO: Calibrate ADC
    // Better resoults when not "calibrated"

    // Timer interrupt
    if (!ITimer0.attachInterruptInterval(READ_INTERVAL_MS * 1000, TimerHandler0))
        // Timer0 failed to attach, this should never happen
        // but in case it does, let's print out some debug info
        Serial.println("Error attaching timer0 interrupt");
}

float read_adc() {
    unsigned long sum_adc = 0;

    for (int i = 0; i < NUM_SAMPLES; i++) {
        sum_adc += analogRead(ANALOG_PIN);
        delay(READ_DELAY_MS);
    }

    return float(sum_adc) / NUM_SAMPLES;
}

float read_temperature() {
    float adc_val = read_adc();

    // Convert adc_val to resistance
    float resistance = 0.0;
    resistance = circuit_slope * adc_val + circuit_intercept;

    // Convert resistance to temperature
    return PT100_SLOPE * resistance + PT100_INTERCEPT;
}

void calibrate() {
    calibrating = true;

    // Wait for calibration mode to be activated
    Serial.println("calibration,0,0,0.0");
    while (digitalRead(CALIBRATION_0_PIN) == HIGH && digitalRead(CALIBRATION_100_PIN) == HIGH) {
        delay(100);
    }

    // Calibration for 0 degrees
    while (digitalRead(CALIBRATION_0_PIN) == HIGH) {
        Serial.println("calibration,0,0,0.0");
        delay(100);
    }
    delay(500);
    float adc_val_0 = read_adc();
    for (int i = 0; i <= 100; i += 10) {
        Serial.println("calibration,0,0," + String(i / 100.0));
        delay(100);
    }

    delay(1000);

    // Calibration for 100 degrees
    Serial.println("calibration,1,0,0.0");
    while (digitalRead(CALIBRATION_100_PIN) == HIGH) {
        Serial.println("calibration,1,0,0.0");
        delay(100);
    }
    delay(500);
    float adc_val_100 = read_adc();
    for (int i = 0; i <= 100; i += 10) {
        Serial.println("calibration,1,0," + String(i / 100.0));
        delay(100);
    }
    Serial.println("calibration,1,1,1");

    // Calculate slope and intercept
    circuit_slope = (RESISTOR_100 - RESISTOR_0) / (adc_val_100 - adc_val_0);
    circuit_intercept = -circuit_slope * adc_val_100 + RESISTOR_100;

    calibrating = false;
}

bool TimerHandler0(struct repeating_timer *t) {
    (void)t;
    if (calibrating)
        return true;

    digitalWrite(LED_PIN, true);
    Serial.println(read_temperature());
    digitalWrite(LED_PIN, false);

    return true;
}

void loop() {
    // if (!calibrated) {
    //     if (Serial.available() > 0) {
    //         String var = Serial.readString();
    //         if (var == "calibrate\n") {
    //             calibrate();
    //         }
    //     }
    // } else {
    //     // for (int i = 0; i < 360; i += 10) {
    //     //     Serial.println(40 * sin(i * PI / 180) + 50);
    //     // }
    //     Serial.println(read_temperature());
    // }
}