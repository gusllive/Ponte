#include <GyverMAX6675.h>
bool mensagemDesligado = false;  // nova variável de controle

//sensor de fluxo
int interrupcao_sensor = 0;
int pino_sensor = 2;

//definição da variável de contagem de voltas
unsigned long contador = 0;

//definição do fator de calibração para conversão do valor lido
const float fator_calibracao = 4.5;

//definição das variáveis de fluxo e volume
float fluxo = 0;
float volume = 0;
float volume_total = 0;

//definição da variável de intervalo de tempo
unsigned long tempo_antes = 0;

// Pinos do sensor ultrassônico
float trig = 4.0;
float eco = 5.0;
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
  pinMode(pino_sensor, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pino_sensor), contador_pulso, FALLING);
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
    mensagemDesligado = false;

    // --- ULTRASSÔNICO ---
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

    // --- TEMPERATURA ---
    float tempAcumula = 0.0;
    int tempValidas = 0;
    float tempAtual = 0.0;
    float tempAnterior = 0.0;

    for (int i = 0; i < 5; i++) {
      if (sens.readTemp()) {
        tempAtual = sens.getTemp() - 1.0;
        if (tempAnterior == 0.0 || tempAtual <= tempAnterior * 1.2) {
          tempAcumula += tempAtual;
          tempAnterior = tempAtual;
          tempValidas++;
        }
      }
      delay(150);
    }

    if (tempValidas > 0) {
      float tempMedia = tempAcumula / tempValidas;
      Serial.print("Temp: ");
      Serial.print(tempMedia);
      Serial.println(" *C");
    } else {
      Serial.println("Erro na leitura da temperatura");
    }

    // --- FLUXO ---
    float fluxoAcumulado = 0.0;
    float fluxoAnterior = 0.0;
    int leiturasValidas = 0;
    contador = 0;
    tempo_antes = millis();

    while (leiturasValidas < 5) {
      contador = 0;
      tempo_antes = millis();

      attachInterrupt(digitalPinToInterrupt(pino_sensor), contador_pulso, FALLING);
      delay(1000);
      detachInterrupt(digitalPinToInterrupt(pino_sensor));

      fluxo = ((1000.0 / (millis() - tempo_antes)) * contador) / fator_calibracao;

      if (fluxoAnterior == 0.0 || fluxo <= fluxoAnterior * 1.2) {
        fluxoAcumulado += fluxo;
        fluxoAnterior = fluxo;
        leiturasValidas++;
      }

      delay(200);
    }

    float fluxoMedio = fluxoAcumulado / 5.0;
    float volumeLido = fluxoMedio / 60.0;
    volume_total += volumeLido;

    Serial.print("Fluxo Médio: ");
    Serial.print(fluxoMedio);
    Serial.println(" L/min");

    Serial.print("Volume Total: ");
    Serial.print(volume_total);
    Serial.println(" L");
    Serial.println();

    delay(1000);

  } else {
    if (!mensagemDesligado) {
      Serial.println("Sistema Desligado");
      mensagemDesligado = true;
    }
  }

  delay(100);
}

void contador_pulso() {
  contador++;
}
