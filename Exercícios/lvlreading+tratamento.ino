
void setup() {
  Serial.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(eco, INPUT);
}

void loop() {
  long duration, previousDuration = 0, inches, cm, acumula = 0;
  int validReadings = 0;

  while (validReadings < 3) {
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(5);
    digitalWrite(trig, LOW);
    duration = pulseIn(eco, HIGH);

    // Se for a primeira leitura ou se a variação for aceitável
    if (previousDuration == 0 || duration <= previousDuration * 1.3) {
      acumula += duration;
      previousDuration = duration;
      validReadings++;
      delay(100); // atraso apenas após uma leitura válida
    }
    // Caso contrário, simplesmente ignora e volta ao while
  }

  acumula = acumula / 3; // média das leituras válidas

  inches = acumula / 74 / 2;
  cm = acumula / 29 / 2;

  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();

  delay(100);
}
