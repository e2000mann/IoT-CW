# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Testing Code

# imports
import time
import datetime
import random
import sys
import pygame


# subroutines
def key_press():
    choice = random.choice(list(button_keys))
    print("Please press {}".format(choice))
    start_time = datetime.datetime.now()

    for event in pygame.event.get():
        print("event {}".format(event.type))
        value = ""

        if event.type == pygame.JOYBUTTONUP:
            value = check_key_value(event, button_keys)
            print("{} key pressed".format(value))

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 4:
                value = "L2"
                print("L2 pressed")
            if event.axis == 5:
                value = "R2"
                print("R2 pressed")

        if choice == value:
            end_time = datetime.datetime.now()
            time_diff = (end_time - start_time)
            latency = time_diff.total_seconds() * 1000
            print("Latency is {}ms".format(latency))

            return True


def check_key_value(event, button_keys):
    for key in button_keys:
        if event.button == key[1]:
            return key[0]

# main section - initialise pygame, no GUI needed
print("code started at {}".format(datetime.datetime.now()))
pygame.init()
# check if controller exists
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    # exit if no controller plugged in
    print("No controller is plugged in!")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()

button_keys = {
    "cross": 0,
    "circle": 1,
    "square": 2,
    "triangle": 3,
    "share": 4,
    "PS": 5,
    "options": 6,
    "L1": 9,
    "R1": 10,
    "up": 11,
    "down": 12,
    "left": 13,
    "right": 14,
    "touchpad": 15,
    "L2": -1,
    "R2": -1
}
# pygame treats L2 and R2 as joystick axes

print(button_keys)

for i in range(20):
    press = key_press()

print("code ended at {}".format(datetime.datetime.now()))
pygame.quit()

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
