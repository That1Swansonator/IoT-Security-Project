int greenLED = 7;
int redLED = 8;
String hvacMode = "off";

void setup() {
  // put your setup code here, to run once:
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);

  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  hvacMode = Serial.readString();

  // Code OFF
  if(hvacMode == "off"){
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, LOW);
    Serial.println(" HVAC Mode: OFF");
  }

  // Code AC
  if (hvacMode == "ac"){
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
    Serial.println(" HVAC Mode: AC");
}

// Code HC
if (hvacMode == "hc"){
  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, HIGH);
  Serial.println(" HVAC Mode: Heat");
}

}
