#include <GyverMAX6675.h>

// Controle do botão
const int BUTTON_PIN = 9;
int estadoBotao = 0; 
bool ultimoEstadoBotao = HIGH;
bool sistemaDesligadoImpressao = true;
bool mensagemDesligado = false;

// Controle do relé
const int rele = 5;

// Sensor de fluxo YF-S401
const byte flowSensorPin = 2; 
volatile unsigned int pulseCount = 0;
float cali = 30.8;  // fator de calibração
unsigned long oldTime = 0;
float flowRate = 0.0;

// Controle de tempo
unsigned long tempoAnterior = 0;
unsigned long intervalo = 1000;
int calibracao_tempo = 2500;

// Sensor ultrassônico
const int trig = 7;
const int eco  = 3;
float valor = 0.0;
float valor2 = 0.0;              // nível convertido (litros)
unsigned long tempoUltrassom = 0;
const unsigned long intervaloUltrassom = 500; // ms

// Sensor de temperatura MAX6675
#define CLK_PIN 13 //SCK
#define DATA_PIN 11 // SO
#define CS_PIN 12 
GyverMAX6675<CLK_PIN, DATA_PIN, CS_PIN> sens;
unsigned long tempoTemp = 0;
const unsigned long intervaloTemp = 800; // ms
float tempMedia = 0.0;            // média de temperatura
void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(trig, OUTPUT);
  pinMode(eco, INPUT);
  pinMode(flowSensorPin, INPUT_PULLUP);
  pinMode(rele, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING);
  oldTime = millis();
  tempoUltrassom = millis();
  tempoTemp = millis();
}
void lerTemp(){
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
      delay(5); // pequeno intervalo entre leituras
    }

    if (tempValidas > 0) {
      tempMedia = tempAcumula / tempValidas;
    } else {
      Serial.println("Erro na leitura da temperatura");
    }
  }
}
void lerLvl(){
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

      unsigned long duration = pulseIn(eco, HIGH, 25000); // timeout para não travar
      if (duration > 0 && (previousDuration == 0.0 || duration <= previousDuration * 1.3)) {
        acumula += duration;
        previousDuration = duration;
        leiturasValidas++;
      }
      delay(5);
    }

    if (leiturasValidas > 0) {
      float cm = (acumula / leiturasValidas) / 29.0 / 2.0;
      valor = (16 - cm);
      valor2 = valor * 1.037 + 0.145;
    }
  }
}
void lerFlow(){
  unsigned long tempoDecorrido = millis() - oldTime;
  if (millis() - oldTime >= 1000) {
    detachInterrupt(digitalPinToInterrupt(flowSensorPin));
    flowRate = ((1000.0 / tempoDecorrido) * pulseCount) / cali;
    pulseCount = 0;
    oldTime = millis();
    attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, FALLING);
  }
}
void printDados(){
  // Imprime os três valores (vazão, nível, temperatura)
  Serial.print(flowRate);
  Serial.print("F ,");

  Serial.print(valor2);
  Serial.print("L ,");

  Serial.print(tempMedia);
  Serial.println("T");
}
void loop() {
  byte buttonState = digitalRead(BUTTON_PIN);

  // Controle do botão (toggle liga/desliga) com debouncing simples
  if (buttonState == LOW && ultimoEstadoBotao == HIGH) {
    estadoBotao = !estadoBotao; 
    delay(50); // debouncing rápido
  }
  ultimoEstadoBotao = buttonState;

  // Sistema Ligado
  if (estadoBotao == 1) {
    mensagemDesligado = false;
    lerTemp();
    lerLvl();
    lerFlow();

    // Controle do relé baseado no nível
  digitalWrite(rele, LOW);    

    printDados();
    delay(1000);
    sistemaDesligadoImpressao = true;
  }
  // Sistema Desligado
  else if (estadoBotao == 0 && sistemaDesligadoImpressao) {
    Serial.println("Sistema desligado");
    sistemaDesligadoImpressao = false;
  }
}
void countPulse(){
  pulseCount++;
}
