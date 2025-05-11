
// Exemplo de código usando millis()
// Inicia variáveis de tempo
unsigned long millisTarefa1 = millis();
unsigned long millisTarefa2 = millis();
// Iniciação
void setup() {
  // Inicia comunicação na porta serial
  Serial.begin(9600);
  // Define pinos dos leds como saída
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
}
// Laço perpétuo
void loop() {
  // Executa tarefa 1
  tarefa1();
  // Executa tarefa 2
  tarefa2();
}
void tarefa1() {
  // Verifica se já passou 200 milisegundos
  if ((millis() - millisTarefa1) < 200) {
    // Acende o led do pino 7
    digitalWrite(7, HIGH);
  } else {
    // Apaga o led do pino 7
    digitalWrite(7, LOW);
  }
  // Verifica se já passou 400 milisegundos
  if ((millis() - millisTarefa1) > 400) {
    millisTarefa1 = millis();
  }
}
void tarefa2() {
  // Verifica se já passou 1000 milisegundos
  if ((millis() - millisTarefa2) < 1000) {
    // Acende o led do pino 8
    digitalWrite(8, HIGH);
  } else {
    // Apaga o led do pino 8
    digitalWrite(8, LOW);
  }
  // Verifica se já passou 2000 milisegundos
  if ((millis() - millisTarefa2) > 2000) {
    millisTarefa2 = millis();
  }
}
