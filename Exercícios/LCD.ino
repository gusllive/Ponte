// Printando informações em um display pela porta serial do arduino 
String leitura
#include <wire.h>                // biblioteca responsável pela comunicação serial do arduino
#include <LiquidCriystal_I2C.h>  // cria funções do LCD
LiquidCriystal_I2C lcd(0x27, 16, 2);  // criou-se um display de 16 colunas e 2 linhas
void setup() {
  lcd.begin();
  Serial.begin(9600);
  lcd.backlight();
  lcd.print("Hello, world")
}
void loop() {
leitura = "";
  while (Serial.available() > 0){
    lcd.clear();
    lcd.print("Hello, world!")
    leitura = Serial.readString();
    lcd.setCursos(0,1);
    lcd.print(leitura);
  }
}
