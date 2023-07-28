void setup() {
    Serial.begin(9600);
}

void loop() {
    for (int i = 0; i < 360; i += 10){
        Serial.println(40*sin(i*PI/180) + 50);
    }
}
