// codigo para L298N
int ang1 = 0, ang2 = 0;
int ult1 = -1, ult2 = -1;


//declaracao dos pinos utilizados para controlar a velocidade de rotacao
const int PINO_ENA = 6; 
const int PINO_ENB = 5;

//declaracao dos pinos utilizados para controlar o sentido do motor
const int PINO_IN1 = 4; 
const int PINO_IN2 = 3;
const int PINO_IN3 = 8;
const int PINO_IN4 = 7;

void setup() {
  Serial.begin(9600);
  pinMode(PINO_ENA, OUTPUT); 
  pinMode(PINO_ENB, OUTPUT);
  pinMode(PINO_IN1, OUTPUT);
  pinMode(PINO_IN2, OUTPUT);
  pinMode(PINO_IN3, OUTPUT);
  pinMode(PINO_IN4, OUTPUT);

  //inicia o codigo com os motores parados
  digitalWrite(PINO_IN1, LOW); 
  digitalWrite(PINO_IN2, LOW);
  digitalWrite(PINO_IN3, LOW);
  digitalWrite(PINO_IN4, LOW);
  digitalWrite(PINO_ENA, LOW);
  digitalWrite(PINO_ENB, LOW);

}

void loop() {
  ang1 = map(analogRead(A0), 0, 1023, 0, 255);
  ang2 = map(analogRead(A1), 0, 1023, 0, 255);
  
  digitalWrite(PINO_IN1, LOW); 
  digitalWrite(PINO_IN2, HIGH);
  digitalWrite(PINO_IN3, LOW);
  digitalWrite(PINO_IN4, HIGH);

  analogWrite(PINO_ENA, ang1);
  analogWrite(PINO_ENB, ang2);

}
