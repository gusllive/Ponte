// Motor
int vaz = 1300; //MIN-0;MAX-1023 Tensão

// Pinos PWM
const int PINO_ENA = 6;
const int PINO_IN1 = 4;
const int PINO_IN2 = 3;

// Sensor de fluxo YF-S401
const byte flowSensorPin = 2; 
volatile unsigned int pulseCount = 0; //Quantidade de Pulsos 
float cali = 30.8;  // fator de calibração
unsigned long oldTime = 0;
float flowRate = 0.0; //Vazão

void setup()
{
  Serial.begin(9600);

  // Motor
  pinMode(PINO_ENA, OUTPUT);
  pinMode(PINO_IN1, OUTPUT);
  pinMode(PINO_IN2, OUTPUT);

  digitalWrite(PINO_IN1, LOW);
  digitalWrite(PINO_IN2, LOW);
  analogWrite(PINO_ENA, 0);

  // Sensor
  pinMode(flowSensorPin, INPUT_PULLUP);

  // INICIA INTERRUPÇÃO (ESSENCIAL)
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, FALLING);
}

void lerFlow() {
  unsigned long tempoDecorrido = millis() - oldTime;

  if (tempoDecorrido >= 1000) {
    detachInterrupt(digitalPinToInterrupt(flowSensorPin));

    flowRate = ((1000.0 / tempoDecorrido) * pulseCount) / cali;

    pulseCount = 0;
    oldTime = millis();

    attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, FALLING);
  }
}

void loop() {
  lerFlow();

  ang1 = map(vaz, 0, 1023, 0, 255);

  digitalWrite(PINO_IN1, LOW);
  digitalWrite(PINO_IN2, HIGH);
  analogWrite(PINO_ENA, ang1);

  Serial.println(flowRate);

  delay(500);
}

// FUNÇÃO DA INTERRUPÇÃO (CORRETA)
void countPulse() {
  pulseCount++;
}