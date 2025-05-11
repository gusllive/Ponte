int memoria = 0

  void
  setup() {
  pinMode(2, INPUT_PULLUP);
  pinMode(13, OUTPUT);

  pinMode(4, INPUT_PULLUP);
  pinMode(5, OUTPUT);

  DigitalWrite(5, 1);
  DigitalWrite(13, 0);
  AnalogWrite(9, 0)

    Serial.begin(9600)
}
void loop() {

  //int memoria [se eu criar uma variável memória neste local, esta memória funcionará apenas dentro do loop e toda vez que o loop
  //encontrar esta variável, ira zerar a mermória.]

  if (digitalRead(2) == 0) {  //ligar o processo com a tecla 2
    memoria = 1;
  }
  if (digitalRead(4) == 0) {  //desligar o processo com a tecla 4
    memoria = 0;
  }
  if (memoria == 1) {

    Serial.println(Analog.Read(A1))
      // alarme de baixa
      if (analog.Read(A1) < 204) {
      DigitalWrite(5, 0);
      DigitalWrite(13, 1);
      AnalogWrite(9, 0);
    }
    // alarme de alta
    else if (Analog.Read(A1) > 812) {
      DigitalWrite(5, 0);
      DigitalWrite(13, 0);
      AnalogWrite(9, 0);
    }
    else {
      DigitalWrite(5, 1);
      DigitalWrite(13, 0);
      AnalogWrite(9, AnalogRead(A1) / 4);
    }
  } else {
    DigitalWrite(5, 1);
    DigitalWrite(13, 0);
    AnalogWrite(9, 0);
  }
}
