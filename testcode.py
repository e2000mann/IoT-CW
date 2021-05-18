# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Testing Code

#imports
import datetime
import random
from approxeng.input.selectbinder import ControllerResource

#global variable - DS4 button name : library button name
all_buttons = {
    'CROSS': 'cross',
    'CIRCLE': 'circle',
    'TRIANGLE': 'triangle',
    'SQUARE': 'square',
    'L1': 'l1',
    'R1': 'r1',
    'L2': 'l2',
    'R2': 'r2',
    'SHARE': 'select',
    'OPTIONS': 'start',
    'PS': 'home',
    'UP': 'dup',
    'RIGHT': 'dright',
    'LEFT': 'dleft',
    'DOWN': 'ddown'
}


#subroutines
def key_press():
    list_buttons = list(all_buttons.items())
    choice = random.choice(list_buttons)
    print("Please press {}".format(choice[0]))
    start_time = datetime.datetime.now()
    completed = False

    while not completed:
        presses = joystick.check_presses()

        if choice[1] in presses:
            completed = True

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    latency = time_diff.total_seconds() * 1000
    print("Latency is {}ms".format(latency))
    return latency


print("code started at {}".format(datetime.datetime.now()))

with ControllerResource() as joystick:
    if joystick.connected:
        latency = []
        for i in range(20):
            latency.append(key_press())

        print("Average latency is {}ms".format(sum(latency)/20))

print("code ended at {}".format(datetime.datetime.now()))
