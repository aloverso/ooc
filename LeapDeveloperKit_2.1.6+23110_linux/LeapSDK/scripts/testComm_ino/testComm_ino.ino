int state = 0;
String incomingString = "";

void setup()
{

  Serial.begin(9600);

}
void loop()
{
  if (state == 0) 
  {
    if (Serial.available()>0)
    {
      byte incoming = Serial.read();
      if(char(incoming) == '@')
      {
        state = 1;
      }
      else
      {
        incomingString += char(incoming);
        Serial.println(incomingString);
      }
      
  }
    
    
  }

}
