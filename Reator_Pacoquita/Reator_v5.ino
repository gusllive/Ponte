//Controle do botão
int BUTTON_PIN = 9;
int estadoBotao = 0; // Variável que armazena o estado do botão (1 ou 0)
bool ultimoEstadoBotao = HIGH; // Guarda o estado anterior do botão
bool botaoAtualmentePressionado = false;
bool sistemaDesligadoImpressao = true; // Variável para garantir que "Sistema desligado" só seja impresso uma vez

#include <GyverMAX6675.h>
bool mensagemDesligado = false;  // nova variável de controle

//Controle do relé
int rele = 5;

// Pino de sinal do YF-S401
const byte flowSensorPin = 2; // deve ser um pino com suporte a interrupção (ex: 2 no Arduino Uno)

// Contador de pulsos, usado na interrupção
volatile unsigned int pulseCount = 0;

//Fator de calibração
float cali = 30.8;

// Tempo de medição
unsigned long oldTime = 0;

// Resultado da vazão
float flowRate = 0;

//Medição de tempo
unsigned long tempoAnterior = 0;
unsigned long intervalo = 1000;
int calibracao_tempo = 2500;
 
// Pinos do sensor ultrassônico
float trig = 7.0;
float eco = 3.0;
float valor = 0.0;

// Pinos do sensor de temperatura
#define CLK_PIN 13
#define DATA_PIN 11
#define CS_PIN 12

GyverMAX6675<CLK_PIN, DATA_PIN, CS_PIN> sens;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Configura o pino do botão com resistor de pull-up interno
  pinMode((int)trig, OUTPUT);
  pinMode((int)eco, INPUT);
  pinMode(flowSensorPin, INPUT_PULLUP); // recomenda-se usar o pull-up interno
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING); // ou FALLING dependendo do sensor
  oldTime = millis();
}

void loop() {
  byte buttonState = digitalRead(BUTTON_PIN); // Lê o estado do botão
  float duration, previousDuration = 0.0, cm, acumula = 0.0;
  float validReadings = 0.0;
  // Verifica se o botão foi pressionado (transição de HIGH para LOW)
  if (buttonState == LOW && ultimoEstadoBotao == HIGH) {
    // Alterna entre 1 e 0
    estadoBotao = (estadoBotao == 0) ? 1 : 0;
    delay(200); // Delay para debouncing
  }

  if (estadoBotao == 1) {
    validReadings = 0;
    acumula = 0.0;
    previousDuration = 0.0;
    mensagemDesligado = false;
    
    unsigned long tempoAtual = millis();

    if (millis() - oldTime >= 1000) { // mede a cada 1 segundo
    // Desabilita interrupção temporariamente para leitura segura
    detachInterrupt(digitalPinToInterrupt(flowSensorPin));

    // Cálculo da vazão em L/min
    // 7.5 pulsos por segundo = 1 L/min (fator típico do YF-S401)
    flowRate = pulseCount / cali;

    //Serial.print("Vazão: ");
    Serial.print(flowRate); 
    Serial.print(",");

    // Zera contador e reinicia tempo
    pulseCount = 0;
    oldTime = millis();

    // Reanexa a interrupção
    attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING);
  }
    if(tempoAtual -tempoAnterior >=intervalo){
      tempoAnterior = tempoAtual;
      unsigned long tempoSegundos = tempoAtual/calibracao_tempo;
      //Serial.print("Tempo:  ");
      //Serial.print(tempoSegundos);
      //Serial.println(",  ");
    }

    while (validReadings < 5.0) { //exemplo usando while
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
    valor = (16 - cm);
    //Serial.print("Nível:  ");    
    Serial.print(valor*1.037+0.145);
    Serial.print(",");
    // Tratamento do sensor de temperatura
    float tempAcumula = 0.0;
    int tempValidas = 0;
    float tempAtual = 0.0;
    float tempAnterior = 0.0;

    for (int i = 0; i < 5; i++) { //exemplo usando o for
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
      //Serial.print("Temp: ");
      Serial.print(tempMedia);
      Serial.println(",");
      //Serial.println("----------------------------------------------------------------------------------");
    } else {
      Serial.println("Erro na leitura da temperatura");
    }

    delay(100);

    sistemaDesligadoImpressao = true; // Reseta a impressão do "Sistema desligado"
  }
  // Se o estado do botão for 0 e ainda não foi impresso "Sistema desligado"
  else if (estadoBotao == 0 && sistemaDesligadoImpressao) {
    Serial.println("Sistema desligado");
    sistemaDesligadoImpressao = false; // Impede mais impressões de "Sistema desligado"
  }

  ultimoEstadoBotao = buttonState;
  delay(100); // Delay para evitar leituras rápidas demais
}
void countPulse() {
  pulseCount++;
}
