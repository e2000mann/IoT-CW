import time
import datetime
import random
import sys
import inputs


# subroutines
def key_press():
    choice = random.choice(all_buttons)
    print("Please press {}".format(choice))
    start_time = datetime.datetime.now()
    completed = False

    while not completed:
        events = inputs.get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)

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

for i in range(20):
    press = key_press()
