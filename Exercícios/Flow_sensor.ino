// Pino de sinal do YF-S401
const byte flowSensorPin = 2; // deve ser um pino com suporte a interrupção (ex: 2 no Arduino Uno)

// Contador de pulsos, usado na interrupção
volatile unsigned int pulseCount = 0;

// Tempo de medição
unsigned long oldTime = 0;

// Resultado da vazão
float flowRate = 0;

void setup() {
  Serial.begin(9600);
  pinMode(flowSensorPin, INPUT_PULLUP); // recomenda-se usar o pull-up interno
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING); // ou FALLING dependendo do sensor
  oldTime = millis();
}

void loop() {
  if (millis() - oldTime >= 1000) { // mede a cada 1 segundo
    // Desabilita interrupção temporariamente para leitura segura
    detachInterrupt(digitalPinToInterrupt(flowSensorPin));

    // Cálculo da vazão em L/min
    // 7.5 pulsos por segundo = 1 L/min (fator típico do YF-S401)
    flowRate = pulseCount / 7.5;

    Serial.print("Vazão: ");
    Serial.print(flowRate);
    Serial.println(" L/min");

    // Zera contador e reinicia tempo
    pulseCount = 0;
    oldTime = millis();

    // Reanexa a interrupção
    attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING);
  }
}

// Função de interrupção chamada a cada pulso
void countPulse() {
  pulseCount++;
}
