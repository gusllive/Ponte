#include "Max6675.h"
 
Max6675 ts(8, 9, 10);
// Max6675 module: SO on pin #8, SS on pin #9, CSK on pin #10 of Arduino UNO

void setup()
{
  ts.setOffset(0);
  // set offset for temperature measurement.
  Serial.begin(9600);
}
 
void loop()
{
  Serial.print(ts.getCelsius(), 2);
  Serial.print(" C / ");
  Serial.print(ts.getFahrenheit(), 2);
  Serial.print(" F / ");
  Serial.print(ts.getKelvin(), 2);
  Serial.print(" Kn");
  Serial.println();
  delay(2000);
