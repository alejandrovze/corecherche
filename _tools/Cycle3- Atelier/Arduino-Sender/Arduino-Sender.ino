// OUTPUTS 14 BUTTONS as 0 / 1 list (e.g. 0 0 0 1 0 0 0 0 1 ...)

int sensorVal[14];

void setup() {

  //start serial connection

  Serial.begin(9600);

  //configure pin 2 as an input and enable the internal pull-up resistor

  for (int i = 2; i < 14; ++i) {
    pinMode(i, INPUT_PULLUP);
  }

}

void loop() {

  for (int i = 2; i < 14; ++i) {
  
    sensorVal[i] = !digitalRead(i);
    Serial.print(sensorVal[i]);
    Serial.print(" ");
  }
  Serial.println();
  delay(100);

}
