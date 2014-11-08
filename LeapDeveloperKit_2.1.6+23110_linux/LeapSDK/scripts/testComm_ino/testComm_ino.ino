int state = 0;
String incomingString = "";

void setup()
{

  Serial.begin(9600);
  pinMode(A0, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode( 9, OUTPUT);
  
  analogWrite(A0, 0);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
}


void ledsOn(int whichOne)
{
  switch(whichOne)
  {
    case 0:
    {
      //digitalWrite(2, LOW);
      analogWrite(A0, 0);
      digitalWrite(3, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      Serial.println("case0");
    }
    case 1:
    {
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
    }
    case 2:
    {
      //digitalWrite(2, HIGH);
      analogWrite(A0,254);
    }
    case 3:
    {
      digitalWrite(3, HIGH);
      
    }
    case 4:
    {
      digitalWrite(4, HIGH);
      
    }
    case 5:
    {
      digitalWrite(5, HIGH);
      
    }
    case 6:
    {
      digitalWrite(6, HIGH);
      
    }
    case 7:
    {
      digitalWrite(7, HIGH);
      
    }
    case 8:
    {
      digitalWrite(8, HIGH);
      
    }
    case 9:
    {
      digitalWrite(9, HIGH);
      
    }
  }
}
void loop()
{
  
    if (Serial.available()>0)
    {
      byte incoming = Serial.read();
      if(char(incoming) == '@')
      {
        ledsOn(incomingString.toInt());
        //delay(500);
        incomingString = "";
        
      }
      else
      {
        incomingString += char(incoming);
        Serial.println(incomingString);
      }
      
    }
    
    
    

}
