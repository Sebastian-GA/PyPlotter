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

// Pin definitions
#define LED_PIN 25
#define ANALOG_PIN 28
#define CALIBRATION_0_PIN 22
#define CALIBRATION_100_PIN 21

// ADC Definitions
#define NUM_SAMPLES 500
#define READ_DELAY 1

// PT100 Calibration
#define PT100_SLOPE 2.730021
#define PT100_INTERCEPT -284.474438

// CIRCUIT Calibration
#define RESISTOR_0 100.7
#define RESISTOR_100 137.7
float circuit_slope = 0.04;  // Default values
float circuit_intercept = 99.55;

bool calibrated = false;

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

    // Calibration
    // TODO: Calibrate ADC
}

float read_voltage() {
    float sum_volt = 0.0;

    for (int i = 0; i < NUM_SAMPLES; i++) {
        sum_volt += float(analogRead(ANALOG_PIN));
        delay(READ_DELAY);
    }

    return sum_volt / NUM_SAMPLES;
}

float read_temperature() {
    float voltage = read_voltage();

    // Convert voltage to resistance
    float resistance = 0.0;
    resistance = circuit_slope * voltage + circuit_intercept;

    // Convert resistance to temperature
    return PT100_SLOPE * resistance + PT100_INTERCEPT;
}

void calibrate() {
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
    float voltage_0 = read_voltage();
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
    float voltage_100 = read_voltage();
    for (int i = 0; i <= 100; i += 10) {
        Serial.println("calibration,1,0," + String(i / 100.0));
        delay(100);
    }
    Serial.println("calibration,1,1,1");

    // Calculate slope and intercept
    circuit_slope = (RESISTOR_100 - RESISTOR_0) / (voltage_100 - voltage_0);
    circuit_intercept = -circuit_slope * voltage_100 + RESISTOR_100;

    calibrated = true;
}

void loop() {
    if (!calibrated) {
        if (Serial.available() > 0) {
            String var = Serial.readString();
            if (var == "calibrate\n") {
                calibrate();
            }
        }
    } else {
        // for (int i = 0; i < 360; i += 10) {
        //     Serial.println(40 * sin(i * PI / 180) + 50);
        // }
        Serial.println(read_temperature());
    }
}