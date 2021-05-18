// up887818
// IOT Coursework - Creating IOT Application for Video Game Controller
// Receiver Code
// Works with Arduino Leonardo (& theoretically Arduino Micro)

#include <SoftwareSerial.h> // serial library
SoftwareSerial mySerial(10, 11); // rx = 10, tx = 11

#include <Joystick.h> // joystick library
// make sure to get the joystick library from
// https://github.com/MHeironimus/ArduinoJoystickLibrary/tree/version-2.0
// please don't use the joystick library in the Arduino IDE's
// library manager, it won't work :)

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, JOYSTICK_TYPE_GAMEPAD,
                   16, 2,                  // 16 Buttons, 2 Joysticks
                   true, true, false,    // X and Y axes, no Z axis
                   false, false, false,    // No Rx, Ry, or Rz
                   false, false,           // No rudder or throttle
                   false, false, false);   // No accelerator, brake, or steering

#include <HID_Buttons.h> // improves button manipulation
// documentation says to import after joystick library

// default button values
int buttonLeftValue = 17;
int buttonRightValue = 17;

void setup() {
  // initialise serial setups
  // mySerial: HC-06 to Arduino
  Serial.begin(9600);
  mySerial.begin(9600);
  Serial.println("Bluetooth is on!");

  // initialise joystick
  Joystick.begin();
}

void loop() {
  while (mySerial.available()) {
    delay(3);
    // get type of input & hand from python code
    char inputType = mySerial.read();
    if (inputType == 'B' or inputType == 'J') {
      determineMode(inputType);
    }
  }
}

void determineMode(char inputType) {
  int hand = mySerial.read() - 48;
  String handName;
  if (hand == 0) {
    handName = "left";
  } else {
    handName = "right";
  }
  if (inputType == 'B') {
    button(handName);
  } else {
    joystick(handName);
  }
}

void button(String hand) {
  // button mode
  // subtract 48 as it sees ascii value
  int newValue;
  float temp = getMultiByteValue();
  newValue = temp;

  if (newValue == 17) {
    if (hand == "left") {
      Joystick.releaseButton(buttonLeftValue);
    } else {
      Joystick.releaseButton(buttonLeftValue);
    }
  } else {
    bool alreadyPressed = (newValue == buttonLeftValue) or (newValue == buttonRightValue);
    if (!(alreadyPressed)) {
      if (hand == "left") {
        Joystick.releaseButton(buttonLeftValue);
        buttonLeftValue = newValue;
        Joystick.pressButton(buttonLeftValue);
      } else {
        Joystick.releaseButton(buttonRightValue);
        buttonRightValue = newValue;
        Joystick.pressButton(buttonRightValue);
      }
    }
  }
}

void joystick(String hand) {
  // joystick mode
  delay(3);
  int x = mySerial.read();
  delay(3);
  int y = mySerial.read();
  String str = hand + String(x) + String(y);
  Serial.println(str);
}

float getMultiByteValue() {
  char btData;
  String output;

  bool notAtEnd = true;
  while (notAtEnd) {
    btData = mySerial.read();
    notAtEnd = (btData != 'B') and (btData != 'Q');
    Serial.println(notAtEnd);
    if (notAtEnd) {
      output = output + btData;
    }
  }

  Serial.println(output);

  return output.toFloat();
}