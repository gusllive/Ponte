#include <ezButton.h>
#include <LiquidCrystal_I2C.h>


ezButton bot1(10);  // Botão da Bomba 1
ezButton bot2(9);   // Botão preto
ezButton bot3(13);  // Botão amarelo

// Motor
int ang1 = 0;

//variável vazão
int vaz = 122; //<--------------------------------------- DEFINE A VAZÃO DO SISTEMA QUANDO SELECIONA A OPÇÃO AUTOMÁTICA

//LCD
LiquidCrystal_I2C lcd(0x27,20,4); 

// Pinos PWM
const int PINO_ENA = 6;
const int PINO_IN1 = 4;
const int PINO_IN2 = 3;

// Sensor de fluxo YF-S401
const byte flowSensorPin = 2; 
volatile unsigned int pulseCount = 0;
float cali = 30.8;  // fator de calibração
unsigned long oldTime = 0;
float flowRate = 0.0;

void setup()
{
  Serial.begin(9600);

  //configuração dos botões
  bot1.setDebounceTime(50); //on off
  bot2.setDebounceTime(50); //preto
  bot3.setDebounceTime(50); //amarelo

  //Flow sensor
  pinMode(flowSensorPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), countPulse, RISING);
  oldTime = millis();

  // Motor
  pinMode(PINO_ENA, OUTPUT);
  pinMode(PINO_IN1, OUTPUT);
  pinMode(PINO_IN2, OUTPUT);

  // Começa tudo desligado
  digitalWrite(PINO_IN1, LOW);
  digitalWrite(PINO_IN2, LOW);

  lcd.init();                      
  // Print a message to the LCD.
  lcd.backlight();
  lcd.setCursor(3,0);
  lcd.print("Defina qual o tipo de controle");
  lcd.setCursor(2,1);
  lcd.print("Amarelo = manual");
   lcd.setCursor(0,2);
  lcd.print("Preto = auto");
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

void loop() {
  // Atualização dos botões
  bot1.loop();
  bot2.loop();
  bot3.loop();
  
  // Ler dadis
  lerFlow();

  // Lê potenciômetros
  ang1 = map(analogRead(A4), 0, 1023, 0, 255);

  if (bot1.getState() == LOW && bot2.getState() == LOW) {
    analogWrite(PINO_ENA, ang1);
  }
  else if (bot1.getState() == LOW && bot3.getState() == LOW) {
    analogWrite(PINO_ENA, vaz);
  }
  else {
    analogWrite(PINO_ENA, 0);
  
  Serial.print(flowRate);
  serial.print("esqueci a unidade,  ")
  
