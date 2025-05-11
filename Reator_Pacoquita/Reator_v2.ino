#include <GyverMAX6675.h>

// Pinos do sensor ultrassônico
float trig = 2.0;
float eco = 3.0;
float valor = 0.0;

// Controle por botões
int memoria = 0;
int liga = 8;
int desliga = 9;

// Pinos do sensor de temperatura
#define CLK_PIN 13
#define DATA_PIN 11
#define CS_PIN 12

GyverMAX6675<CLK_PIN, DATA_PIN, CS_PIN> sens;

void setup() {
  Serial.begin(9600);
  pinMode((int)trig, OUTPUT);
  pinMode((int)eco, INPUT);
  pinMode(liga, INPUT_PULLUP);
  pinMode(desliga, INPUT_PULLUP);
}

void loop() {
  float duration, previousDuration = 0.0, cm, acumula = 0.0;
  float validReadings = 0.0;

  if (digitalRead(liga) == 0) {
    memoria = 1;
  }
  if (digitalRead(desliga) == 0) {
    memoria = 0;
  }

  if (memoria == 1) {
    // Tratamento do sensor ultrassônico
    validReadings = 0;
    acumula = 0.0;
    previousDuration = 0.0;
    while (validReadings < 5.0) {
      digitalWrite((int)trig, LOW);
      delayMicroseconds(2);
      digitalWrite((int)trig, HIGH);
      delayMicroseconds(5);
      digitalWrite((int)trig, LOW);
      duration = pulseIn((float)eco, HIGH);

      if (previousDuration == 0.0 || duration <= previousDuration * 1.3) {
        acumula += duration;
        previousDuration = duration;
        validReadings++;
        delay(100);
      }
    }

    cm = (acumula / 5.0) / 29.0 / 2.0;
    valor = 13.0 - cm;
    Serial.print("Nivel: ");
    Serial.print(valor);
    Serial.print(" cm  ");

    // Tratamento do sensor de temperatura
    float tempAcumula = 0.0;
    int tempValidas = 0;
    float tempAtual = 0.0;
    float tempAnterior = 0.0;

    for (int i = 0; i < 5; i++) {
      if (sens.readTemp()) {
        tempAtual = sens.getTemp() - 1.0;  // Correção
        if (tempAnterior == 0.0 || tempAtual <= tempAnterior * 1.2) {
          tempAcumula += tempAtual;
          tempAnterior = tempAtual;
          tempValidas++;
        }
      }
      delay(150);  // tempo entre leituras
    }

    if (tempValidas > 0) {
      float tempMedia = tempAcumula / tempValidas;
      Serial.print("Temp: ");
      Serial.print(tempMedia);
      Serial.println(" *C");
    } else {
      Serial.println("Erro na leitura da temperatura");
    }

    delay(1000);

  } else {
    Serial.println("Sistema Desligado");
  }

  delay(100);
}
