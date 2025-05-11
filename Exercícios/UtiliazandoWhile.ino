//Pino ligado ao push-button
int buttonPin = A0;
//Variavel para fazer a checagem
int buttonState;
// Associando o LEDs aos Pinos correspondentes
int ledAmarelo = A1;
void setup()
  {
  // Inicializar cada pino do LED como saída
  pinMode(ledAmarelo,OUTPUT); 
  // Define o pino do botao como entrada
  pinMode(buttonPin, INPUT);
}
void loop() {
  // Verifica se o estado do botao foi alterado 
  buttonState = analogRead(buttonPin);
  // Limpa qualquer ruido      
  buttonState = 1023;
  // Enquanto nenhum botao está sendo pressionado realiza a leitura novamente
  while (buttonState >= 897)
  {
    //Acende o LED Amarelo
    digitalWrite(ledAmarelo, HIGH);
    buttonState = analogRead(buttonPin);
  } 
  if (buttonState < 897)
    { 
        // Se o botão Right está sendo apertado  
        while (buttonState < 69)
          {
            //Apaga o LED Amarelo
            digitalWrite(ledAmarelo, LOW);
            buttonState = analogRead(buttonPin);        
          } 
      }  
}  
