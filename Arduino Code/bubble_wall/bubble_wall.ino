const byte numChars = 36;
char receivedChars[numChars];

boolean newData = false;
int startPin = 13;
int AirTime = 1000;

void setup() {
  int i;
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Power on!");
  for (i = 0; i <= numChars -1; i++)
  {
    pinMode(i + startPin, OUTPUT);
  }
}

void loop() {
  int i;
  char data[numChars];
  int flag = 0;
  recvWithStartEndMarkers();

  for (i = 0; i <= (numChars - 1); i++)
  {
    if (receivedChars[i] == '1')
    {
      Serial.print(i);
      Serial.print(", ");
      digitalWrite(i + startPin, HIGH);
      receivedChars[i] = 0;
      flag = flag + 1;
    }
    else if (receivedChars[i] == '0')
    {
      Serial.print("*");
      Serial.print(i);
      Serial.print("*, ");
      digitalWrite(i + startPin, LOW);
      receivedChars[i] = 0;
      flag = flag + 1;
    }
  }
  newData = false;
  if (flag != 0)
  {
    //Serial.print(" |   ");
    //Serial.println(flag);
    flag = 0;
  }

  delay(100);

  for (i = 0; i <= (numChars - 1); i++)
  {
      digitalWrite(i + startPin, LOW);
  }
}


void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    if (recvInProgress == true) {

      //Check if need to start the inputs.


      //checking if new msg for the LCD arravied (using start and ending markers).
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}
