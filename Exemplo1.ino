//Exemplo 1
void setup() {
  Serial.begin(9600);
}
void loop() {
  if (analogRead(A0) < 100)
  {
    Serial.print("Leitura A0: ");
    Serial.print(analogRead(A0));
    Serial.print(" - sendo Taxa A, resultando em: R$");
    Serial.println(analogRead(A0) * 4.1 / 10);
  }
  else if (analogRead(A0) >= 100 and analogRead(A0) < 200)
  {
    Serial.print("Leitura A0: ");
    Serial.print(analogRead(A0));
    Serial.print(" - sendo Taxa B, resultando em: R$");
    Serial.println(analogRead(A0) * 4.3 / 10);
  }
  else if (analogRead(A0) >= 200 and analogRead(A0) < 300)
  {
    Serial.print("Leitura A0: ");
    Serial.print(analogRead(A0));
    Serial.print(" - sendo Taxa C, resultando em: R$");
    Serial.println(analogRead(A0) * 4.5 / 10);
  }
    else if (analogRead(A0) >= 300 and analogRead(A0) < 400)
  {
    Serial.print("Leitura A0: ");
    Serial.print(analogRead(A0));
    Serial.print(" - sendo Taxa D, resultando em: R$");
    Serial.println(analogRead(A0) * 4.7 / 10);
  }
    else if (analogRead(A0) >= 400 and analogRead(A0) < 500)
  {
    Serial.print("Leitura A0: ");
    Serial.print(analogRead(A0));
    Serial.print(" - sendo Taxa E, resultando em: R$");
    Serial.println(analogRead(A0) * 4.9 / 10);
  }
    else
  {
    Serial.print("Leitura A0: ");
    Serial.print(analogRead(A0));
    Serial.print(" - sendo Taxa F, resultando em: R$");
    Serial.println(analogRead(A0) * 5.1 / 8);
  }
}
