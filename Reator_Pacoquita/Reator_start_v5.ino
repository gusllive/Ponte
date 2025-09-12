//código lê um botão conectado a entrada 3 do nosso arduino, no exemplo realizado em 12_09_25 foi utilizado um arduino nano
int BUTTON_PIN = 3;
int estadoBotao = 0; // Variável que armazena o estado do botão (1 ou 0)
bool ultimoEstadoBotao = HIGH; // Guarda o estado anterior do botão
bool botaoAtualmentePressionado = false;
bool sistemaDesligadoImpressao = true; // Variável para garantir que "Sistema desligado" só seja impresso uma vez

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Configura o pino do botão com resistor de pull-up interno
}

void loop() {
  byte buttonState = digitalRead(BUTTON_PIN); // Lê o estado do botão

  // Verifica se o botão foi pressionado (transição de HIGH para LOW)
  if (buttonState == LOW && ultimoEstadoBotao == HIGH) {
    // Alterna entre 1 e 0
    estadoBotao = (estadoBotao == 0) ? 1 : 0;

    delay(200); // Delay para debouncing
  }

  if (estadoBotao == 1) {
    Serial.println("Sistema ligado");
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
