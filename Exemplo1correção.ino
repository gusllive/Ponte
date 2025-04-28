int analogica = A4;
String entrada = "A4";
int leitura;
int divisor = 13;
float iniMult = 3.3;
int comeco = 80;
int taxa = 100 void
setup() {
  Serial.begin(9600);
}
void loop() {
  leitura = analogRead(analogica);
  if (leitura < comeco) {
    Serial.print("Leitura ");
    Serial.print(entrada);
    Serial.print(": ");
    Serial.print(leitura);
    Serial.print(" - sendo Taxa A, resultando em: R$");
    Serial.println(leitura * iniMult / divisor);
  } else if (leitura >= comeco + taxa and leitura < comeco + taxa * 2) {
    Serial.print("Leitura ");
    Serial.print(entrada);
    Serial.print(": ");
    Serial.print(leitura);
    Serial.print(" - sendo Taxa B, resultando em: R$");
    Serial.println(leitura * (iniMult + 0.2) / divisor);
  } else if (leitura >= comeco + taxa * 2 and leitura < comeco + taxa * 3) {
    Serial.print("Leitura ");
    Serial.print(entrada);
    Serial.print(": ");
    Serial.print(leitura);
    Serial.print(" - sendo Taxa B, resultando em: R$");
    Serial.println(leitura * (iniMult + 0.6) / divisor);
  } else if (leitura >= comeco + taxa * 3 and leitura < comeco + taxa * 4) {
    Serial.print("Leitura ");
    Serial.print(entrada);
    Serial.print(": ");
    Serial.print(leitura);
    Serial.print(" - sendo Taxa B, resultando em: R$");
    Serial.println(leitura * (iniMult + 0.8) / divisor);
  } else {
    Serial.print("Leitura A0: ");
    Serial.print(leitura);
    Serial.print(" - sendo Taxa F, resultando em: R$");
    Serial.println(leitura * (iniMult + 1) / (divisor - 2));
  }
}
