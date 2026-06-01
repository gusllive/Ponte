//Controle do botão
int BUTTON_PIN = 9;
int estadoBotao = 0; 
bool ultimoEstadoBotao = HIGH;
bool sistemaDesligadoImpressao = true;

#include <GyverMAX6675.h>
bool mensagemDesligado = false;

//Controle do relé
int rele = 5;

// Sensor de fluxo YF-S401
const byte flowSensorPin = 2; 
volatile unsigned int pulseCount = 0;
float cali = 30.8;  // fator de calibração
unsigned long oldTime = 0;
float flowRate = 0;

// Controle de tempo
unsigned long tempoAnterior = 0;
unsigned long intervalo = 1000;
int calibracao_tempo = 2500;

// Sensor ultrassônico
const int trig = 7;
const int eco  = 3;
float valor = 0.0;
unsigned long tempoUltrassom = 0;
const unsigned long intervaloUltrassom = 500; // ms

// Sensor de temperatura MAX6675
#define CLK_PIN 13
#define DATA_PIN 11
#define CS_PIN 12
GyverMAX6675<CLK_PIN, DATA_PIN, CS_PIN> sens;
unsigned long tempoTemp = 0;
const unsigned long intervaloTemp = 800; // ms

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(trig, OUTPUT);
  pinMode(eco, INPUT);
  pinMode(flowSensorPin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING);
  oldTime = millis();
}

void loop() {
  byte buttonState = digitalRead(BUTTON_PIN);

  // --- Controle do botão (toggle liga/desliga) ---
  if (buttonState == LOW && ultimoEstadoBotao == HIGH) {
    estadoBotao = !estadoBotao; 
    delay(50); // só para debouncing rápido
  }
  ultimoEstadoBotao = buttonState;

  // --- Sistema Ligado ---
  if (estadoBotao == 1) {
    mensagemDesligado = false;

    // --- Vazão a cada 1 segundo ---
    if (millis() - oldTime >= 1000) {
      detachInterrupt(digitalPinToInterrupt(flowSensorPin));
      flowRate = pulseCount / cali;
      Serial.print(flowRate);
      Serial.print(",");
      pulseCount = 0;
      oldTime = millis();
      attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING);
    }

    // --- Medição de tempo de processo ---
    if (millis() - tempoAnterior >= intervalo) {
      tempoAnterior = millis();
      unsigned long tempoSegundos = tempoAnterior / calibracao_tempo;
      //Serial.println(tempoSegundos);
    }

    // --- Leitura ultrassom (a cada intervaloUltrassom ms) ---
    if (millis() - tempoUltrassom >= intervaloUltrassom) {
      tempoUltrassom = millis();
      float acumula = 0.0;
      float previousDuration = 0.0;
      int leiturasValidas = 0;

      for (int i = 0; i < 5; i++) {
        digitalWrite(trig, LOW);
        delayMicroseconds(2);
        digitalWrite(trig, HIGH);
        delayMicroseconds(5);
        digitalWrite(trig, LOW);

        float duration = pulseIn(eco, HIGH, 25000); // timeout para não travar
        if (duration > 0 && (previousDuration == 0.0 || duration <= previousDuration * 1.3)) {
          acumula += duration;
          previousDuration = duration;
          leiturasValidas++;
        }
      }

      if (leiturasValidas > 0) {
        float cm = (acumula / leiturasValidas) / 29.0 / 2.0;
        valor = (16 - cm);
        Serial.print(valor * 1.037 + 0.145);
        Serial.print(",");
      }
    }

    // --- Leitura temperatura (a cada intervaloTemp ms) ---
    if (millis() - tempoTemp >= intervaloTemp) {
      tempoTemp = millis();
      float tempAcumula = 0.0;
      int tempValidas = 0;
      float tempAnterior = 0.0;

      for (int i = 0; i < 5; i++) {
        if (sens.readTemp()) {
          float tempAtual = sens.getTemp() - 1.0;
          if (tempAnterior == 0.0 || tempAtual <= tempAnterior * 1.2) {
            tempAcumula += tempAtual;
            tempAnterior = tempAtual;
            tempValidas++;
          }
        }
      }

      if (tempValidas > 0) {
        float tempMedia = tempAcumula / tempValidas;
        Serial.print(tempMedia);
        Serial.println(",");
      } else {
        Serial.println("Erro na leitura da temperatura");
      }
    }

    sistemaDesligadoImpressao = true;
  }

  // --- Sistema Desligado ---
  else if (estadoBotao == 0 && sistemaDesligadoImpressao) {
    Serial.println("Sistema desligado");
    sistemaDesligadoImpressao = false;
  }
}

void countPulse() {
  pulseCount++;
}
