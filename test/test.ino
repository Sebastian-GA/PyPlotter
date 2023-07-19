bool calibrated = false;

void setup() {
    Serial.begin(9600);
}

void loop() {
    if (!calibrated) {
        if (Serial.available() > 0){
            String var = Serial.readString();
            if (var == "calibrate\n"){
                for (int i = 0; i <= 100; i++){
                    Serial.println("calibration,0,0,"+String(i/100.0));
                }
                Serial.println("calibration,1,0,0");
                delay(1000);
                for (int i = 0; i <= 100; i++){
                    Serial.println("calibration,1,0,"+String(i/100.0));
                }
                Serial.println("calibration,1,1,1");
                calibrated = true;
            }   
        }            
    } else {   
        for (int i = 0; i < 360; i += 10){
            Serial.println(40*sin(i*PI/180) + 50);
        }
    }
}
