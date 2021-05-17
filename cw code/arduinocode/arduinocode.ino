// up887818
// IOT Coursework - Creating IOT Application for Video Game Controller
// Receiver Code

#include <SoftwareSerial.h> // serial library
SoftwareSerial mySerial(10, 11); // rx = 10, tx = 11

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  mySerial.begin(9600);

  Serial.println("Bluetooth is on!");
}

void loop() {
  // put your main code here, to run repeatedly:
    while (mySerial.available()) {
        delay(3);
        char inputType = mySerial.read();
        if (inputType == 'B'){
          button();
        } else {
          joystick();
        }
    }
}

void button(){
  // button mode
  delay(3);
  int button = mySerial.read();
  String str = String(button);
  Serial.println(str);
}

void joystick(){
  // joystick mode
  delay(3);
  int hand = mySerial.read();
  String hand_name;
  if (hand == 0){
    hand_name = "left";
  } else{
    hand_name = "right";
  }
  delay(3);
  int x = mySerial.read();
  delay(3);
  int y = mySerial.read();
  String str = hand_name + String(x) + String(y);
  Serial.println(str);
}
