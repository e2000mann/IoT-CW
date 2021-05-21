# Video Game Controller
Internet of Things coursework 2021

## About
This controller uses a webcam input to detect button presses and joystick movements through gesture recognition/hand positions. It was intended to replicate a DualShock 4 controller and hence has 16 buttons and 2 joysticks (X & Y axes), and the layout shows DS4 buttons. Currently it only shows on the computer as a generic controller but there is a way to get the computer to recognise it as a DualShock 4 (not recommended due to its complexity).

The Arduino must be based on the ATmega32u4 microcontroller so it can be seen as a HID device, therefore only the Leonardo (tested) & Micro (untested) works. A HC-06 module is used to provide bluetooth communication.

## Software/Non-Default Libraries used
Python Libraries:
- maincode.py:
    - cv2 for image manipulation
    - mediapipe for hand recognition
- testcode.py:
    - [Approximate Engineering - Input](https://approxeng.github.io/approxeng.input/index.html) (linux only)
        - The yaml file is a configuration file for this library so that I could test my controller. To use, add it into ~/.approxeng.input/

Arduino Libraries:
- [MHeironimus' ArduinoJoystickLibrary](https://github.com/MHeironimus/ArduinoJoystickLibrary)

Software: 
- Used to emulate DS4 from generic ([following this tutorial](https://forums.vigem.org/topic/272/x360ce-to-vigem))
    - [x360ce](https://www.x360ce.com/)
    - [ViGEmBus](https://github.com/ViGEm/ViGEmBus/)
    - [VDX](https://buildbot.vigem.org/builds/VDX/master/)
- Used to create linux VM for testing:
    - VirtualBox
