#include <ezButton.h>

ezButton bot1(10);   // Botão da Bomba 1
ezButton bot2(13);  // Botão da Bomba 2

// Motores 
int ang1 = 0, ang2 = 0;

// Pinos PWM
const int PINO_ENA = 6;
const int PINO_ENB = 5;

const int PINO_IN1 = 4;
const int PINO_IN2 = 3;
const int PINO_IN3 = 8;
const int PINO_IN4 = 7;

void setup() {
  Serial.begin(9600);

  // Configuração dos botões
  bot1.setDebounceTime(50);
  bot2.setDebounceTime(50);

  // Motores
  pinMode(PINO_ENA, OUTPUT);
  pinMode(PINO_ENB, OUTPUT);
  pinMode(PINO_IN1, OUTPUT);
  pinMode(PINO_IN2, OUTPUT);
  pinMode(PINO_IN3, OUTPUT);
  pinMode(PINO_IN4, OUTPUT);

  // Começa tudo desligado
  digitalWrite(PINO_IN1, LOW);
  digitalWrite(PINO_IN2, LOW);
  digitalWrite(PINO_IN3, LOW);
  digitalWrite(PINO_IN4, LOW);

  analogWrite(PINO_ENA, 0);
  analogWrite(PINO_ENB, 0);
}

void loop() {
  // Atualização dos botões
  bot1.loop();
  bot2.loop();

  // Lê potenciômetros
  ang1 = map(analogRead(A0), 0, 1023, 0, 255);
  ang2 = map(analogRead(A1), 0, 1023, 0, 255);

  // BOMBA 1
  if (bot1.getState() == LOW) { 
    // Botão ON
    digitalWrite(PINO_IN1, LOW);
    digitalWrite(PINO_IN2, HIGH);
    analogWrite(PINO_ENA, ang1);
  } 
  else {
    // Botão OFF
    analogWrite(PINO_ENA, 0);
  }

  // BOMBA 2 
  if (bot2.getState() == LOW) {
    // Botão ON
    digitalWrite(PINO_IN3, LOW);
    digitalWrite(PINO_IN4, HIGH);
    analogWrite(PINO_ENB, ang2);
  } 
  else {
    // Botão OFF
    analogWrite(PINO_ENB, 0);
  }
}
