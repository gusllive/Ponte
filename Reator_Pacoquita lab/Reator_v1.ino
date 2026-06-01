//Teste para aferição do sensor de temperatura MAX-6675 e sensor de nível HC-SR04 com acionamento via botões 
#include <GyverMAX6675.h>
float trig = 2.0;
float eco = 3.0;
float valor = 0.0;
int memoria = 0;
int liga = 8;
int desliga = 9;

#define CLK_PIN 13   // Пин SCK
#define DATA_PIN 11  // Пин SO
#define CS_PIN 12    // Пин CS

GyverMAX6675<CLK_PIN, DATA_PIN, CS_PIN> sens;

void setup() {
  Serial.begin(9600);
  pinMode((int)trig, OUTPUT);  // pinMode still requires int
  pinMode((int)eco, INPUT);
  pinMode(liga, INPUT_PULLUP);
  pinMode(desliga, INPUT_PULLUP);
}

void loop() {
  float duration, previousDuration = 0.0, inches, cm, acumula = 0.0;
  float validReadings = 0.0;

  if (digitalRead(liga) == 0) {
    memoria = 1;
  }
  if (digitalRead(desliga) == 0) {
    memoria = 0;
  }

  if (memoria == 1) {
    while (validReadings < 5.0) {
      digitalWrite((int)trig, LOW);
      delayMicroseconds(2);
      digitalWrite((int)trig, HIGH);
      delayMicroseconds(5);
      digitalWrite((int)trig, LOW);
      duration = pulseIn((float)eco, HIGH);

      // If it's the first reading or the variation is acceptable
      if (previousDuration == 0.0 || duration <= previousDuration * 1.3) {
        acumula += duration;
        previousDuration = duration;
        validReadings++;
        delay(100);  // delay only after a valid reading
      }
    }

    acumula = acumula / 5.0;  // average of valid readings
    cm = acumula / 29.0 / 2.0;

    valor = 13.0 - cm;

    Serial.print(valor);
    Serial.print("cm  ");
  

    if (sens.readTemp()) {
      //Serial.print("Temp: ");
      Serial.print(sens.getTemp()-1);
      //Serial.print(sens.getTempInt());   // или getTempInt - целые числа (без float)
      Serial.println(" *C");
    } else Serial.println("Error");

    delay(1000);

  } else {
    Serial.println("Sistema Desligado");
  }
  delay(100);
}
