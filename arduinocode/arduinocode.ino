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
                   16, 0,                  // 16 Buttons, No HatSwitches
                   true, true, false,      // X and Y axes, no Z
                   true, true, false,      // Rx and Ry axes, no Rz
                   false, false,           // No rudder or throttle
                   false, false, false);   // No accelerator, brake, or steering

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
  // axes ranges
  Joystick.setXAxisRange(-100, 100);
  Joystick.setYAxisRange(-100, 100);
  Joystick.setRxAxisRange(-100, 100);
  Joystick.setRyAxisRange(-100, 100);
  // start joystick
  Joystick.begin();
}

void loop() {
  while (mySerial.available()) {
    delay(3);
    // get type of input & hand from python code
    char inputType = mySerial.read();
    determineMode(inputType);
  }
}

void determineMode(char inputType) {
  int hand = mySerial.read() - 48;
  String handName = hand == 0 ? "left" : "right";
  if (inputType == 'B') {
    button(handName);
  } 
  if (inputType == 'J'){
    joystick(handName);
  }
  if (inputType == 'U'){
    removeMapping(handName);
  }
}

void button(String hand) {
  // button mode
  // subtract 48 as it sees ascii value
  int newValue;
  float temp = getMultiByteValue();
  newValue = temp;
  bool alreadyPressed;
  if (newValue == 17) {
    if (hand == "left") {
      Joystick.releaseButton(buttonLeftValue);
    } else {
      Joystick.releaseButton(buttonLeftValue);
    }
  }
  else {
    if (hand == "left"){
      alreadyPressed = (newValue == buttonRightValue);
      if (!(alreadyPressed)){
        Joystick.releaseButton(buttonLeftValue);
        buttonLeftValue = newValue;
        Joystick.pressButton(buttonLeftValue);
      }
    } else {
      alreadyPressed = (newValue == buttonLeftValue);
      if (!(alreadyPressed)){
        Joystick.releaseButton(buttonRightValue);
        buttonRightValue = newValue;
        Joystick.pressButton(buttonRightValue);
      }
    }
  }
}

//   bool alreadyPressed = (newValue == buttonLeftValue) or (newValue == buttonRightValue);
//     if (!(alreadyPressed)) {
//       if (hand == "left") {
//         Joystick.releaseButton(buttonLeftValue);
//         buttonLeftValue = newValue;
//         Joystick.pressButton(buttonLeftValue);
//       } else {
//         Joystick.releaseButton(buttonRightValue);
//         buttonRightValue = newValue;
//         Joystick.pressButton(buttonRightValue);
//       }
//     }

//   if (newValue == 17) {
//     if (hand == "left") {
//       Joystick.releaseButton(buttonLeftValue);
//     } else {
//       Joystick.releaseButton(buttonLeftValue);
//     }
//   } else {
//     bool alreadyPressed = (newValue == buttonLeftValue) or (newValue == buttonRightValue);
//     if (!(alreadyPressed)) {
//       if (hand == "left") {
//         Joystick.releaseButton(buttonLeftValue);
//         buttonLeftValue = newValue;
//         Joystick.pressButton(buttonLeftValue);
//       } else {
//         Joystick.releaseButton(buttonRightValue);
//         buttonRightValue = newValue;
//         Joystick.pressButton(buttonRightValue);
//       }
//     }
//   }
// }

void joystick(String hand) {
  // joystick mode
  float x = getMultiByteValue();
  float y = getMultiByteValue();
  if (hand == "left"){
    Joystick.setXAxis(x);
    Joystick.setYAxis(y);
  } else {
    Joystick.setRxAxis(x);
    Joystick.setRyAxis(y);
  }
}

void removeMapping(String hand) {
  if (hand == "left"){
    Joystick.releaseButton(buttonLeftValue);
    buttonLeftValue = 17;
  } else {
    Joystick.releaseButton(buttonRightValue);
    buttonLeftValue = 17;
  }
}

float getMultiByteValue() {
  char btData;
  String output = "";

  bool notAtEnd = true;
  while (notAtEnd) {
    btData = mySerial.read();
    notAtEnd = !isAlpha(btData);
    output = notAtEnd ? output + btData : output;
  }

  return output.toFloat();
}
