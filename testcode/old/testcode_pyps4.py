# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Testing Code

# imports
import time
import datetime
import random
import sys

from pyPS4Controller.controller import Controller
from pyPS4Controller.event_mapping.DefaultMapping import DefaultMapping

#classes
class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


class MyEventDefinition(DefaultMapping):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def x_pressed(self):
        print("{} has been pressed".format(self.button_id))

    def x_released(self):
        print("{} has been released".format(self.button_id))


# subroutines
def key_press():
    choice = random.choice(all_buttons)
    print("Please press {}".format(choice))
    start_time = datetime.datetime.now()

    # pressed = False
    # released = False
    #
    # is_button = (choice not in dpad_x and choice not in dpad_y)
    #
    # if is_button:
    #     while not pressed:
    #         pressed = gamepad.beenPressed(choice)
    #         print("{} has been pressed".format(choice))
    #     while not released:
    #         released = gamepad.beenReleased(choice)
    #         print("{} has been released".format(choice))
    #
    # else:
    #     while not pressed:
    #         axis = axis(choice)
    #         if (choice == dpad_x[0] or choice == dpad_y[0]):
    #             pressed = axis == 1
    #         else:
    #             pressed = axis == -1
    #     while not released:
    #         axis = axis(choice)
    #         released = axis == 0
    #
    # end_time = datetime.datetime.now()
    # time_diff = (end_time - start_time)
    # latency = time_diff.total_seconds() * 1000
    # print("Latency is {}ms".format(latency))
    return True


def check_key_value(event, button_keys):
    for key in button_keys:
        if event.button == key[1]:
            return key[0]

# main section - initialise pygame, no GUI needed
print("code started at {}".format(datetime.datetime.now()))

controller = MyController(interface = "/dev/input/js2",
            connecting_using_ds4drv = False)
            # event_definition = MyEventDefinition
controller.listen()

button_keys = [
    'CROSS',
    'CIRCLE',
    'TRIANGLE',
    'SQUARE',
    'L1',
    'R1',
    'L2',
    'R2',
    'SHARE',
    'OPTIONS',
    'PS'
]
# Gamepad treats d-pad as axis
dpad_x = ["RIGHT", "LEFT"]
dpad_y = ["UP", "DOWN"]

all_buttons = button_keys + dpad_x + dpad_y

print(all_buttons)

for i in range(20):
    press = key_press()

print("code ended at {}".format(datetime.datetime.now()))

# cur_time = time.time()
# # end time = 180 seconds (3 minutes) after current time
# end_time = cur_time + 180
#
# while time.time() != end_time:
#     # occurs every 1-5 seconds
#     pause = random.randint(1, 5)
#     time.sleep(pause)
#
#     key_press(controller, button_keys)
