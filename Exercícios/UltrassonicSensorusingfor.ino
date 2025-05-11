int trig = 2;
int eco = 3;

void setup() {

  Serial.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(eco, INPUT);
}
void loop() {
  long duration, inches, cm, acumula = 0;

  for (int i = 0; i < 3; i++) {
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(5);
    digitalWrite(trig, LOW);
    duration = pulseIn(eco, HIGH);

    acumula = acumula + duration;

    delay(100);
  }

  acumula = acumula / 3; // fazendo a média de 3 leituras para diminuir a oscilação

  inches = acumula / 74 / 2;
  cm = acumula / 29 / 2;

  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();

  delay(100);
}
