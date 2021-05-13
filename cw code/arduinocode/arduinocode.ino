#include <SoftwareSerial.h> // serial library
SoftwareSerial mySerial(2, 3); // rx = 2, tx = 3

char BluetoothData; // gets button name from bt

void setup() {
  // put your setup code here, to run once:
  Serial.begin(4800);
  mySerial.begin(9600);
  
  Serial.println("Bluetooth is on!");
  // print instructions
  Serial.println("HC-06 AT Command Programming");
  Serial.println(" -- Command Reference ---");
  Serial.println("AT (simply checks connection)");
  Serial.println("AT+VERSION (sends the firmware verison)");
  Serial.println("AT+NAMExxxxx (to change name to xxxxx");
  Serial.println("AT+PINnnnn (to change password to 4 digit nnnn");
  Serial.println("AT+BAUDn (to change to baud rate #1");
  Serial.println("  BAUD1 = 1200");
  Serial.println("  BAUD2 = 2400");
  Serial.println("  BAUD3 = 4800");
  Serial.println("  BAUD4 = 9600");
  Serial.println("  BAUD5 = 19200");
  Serial.println("  BAUD6 = 38400");
  Serial.println("  BAUD7 = 57600");
  Serial.println("  BAUD8 = 115200");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (mySerial.available()){
    BluetoothData = mySerial.read();
    Serial.print(BluetoothData);
    delay(100); // prepare for next data
  }
}
