# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Main Code

import cv2
import mediapipe as mp
import math
import socket

# global constants
MIN_MOVEMENT_ALLOWANCE = 0.03 # how much hand has to be moved to be new input
INNER_ANNULUS = ["TRIANGLE", "RIGHT", "CIRCLE", "DOWN",
                 "CROSS", "LEFT", "SQUARE", "UP"]
INNER_ANNULUS_START = 0.25
OUTER_ANNULUS = ["OPTIONS", "R2", "R1", "PS",
                 "TOUCHPAD", "L1", "L2", "SHARE"]
OUTER_ANNULUS_START = 0.375
GLOBAL_ORIGIN = (0.5, 0.5)
BUTTON_PLACEHOLDER = 17 # using "17" as placeholder as only 16 buttons
JOY_PLACEHOLDER = (-1, -1)
MAX_JOY_MOVEMENT = 0.25 # how far hand has to go for axis to be -1 or 1
# bluetooth constants (there is a passkey... windows will ask for it)
SERVER_MAC = "00:19:10:09:27:26"
PORT = 1

# global variables
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM,
                 socket.BTPROTO_RFCOMM) # bluetooth socket
# set up mediapipe & cv2
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.6,
                           min_tracking_confidence=0.5)
camera = cv2.VideoCapture(0)
# 0th index is left hand, 1st index is right hand
joy_origins = [JOY_PLACEHOLDER, JOY_PLACEHOLDER]
held_button = [BUTTON_PLACEHOLDER, BUTTON_PLACEHOLDER]
previous_location = [GLOBAL_ORIGIN, GLOBAL_ORIGIN]


def button_mode(hand, palm):
    # clear origin from joystick mode
    joy_origins[hand] = JOY_PLACEHOLDER

    movement = line_distance([previous_location[hand][0], palm[0]],
                            [previous_location[hand][1], palm[1]])

    if MIN_MOVEMENT_ALLOWANCE <= movement:
        print("accept")
        previous_location[hand] = palm
        # check hand's radius (distance) from global origin
        radius = line_distance([GLOBAL_ORIGIN[0], palm[0]],
                              [GLOBAL_ORIGIN[1], palm[1]])

        if radius >= INNER_ANNULUS_START:
            # check how many degrees from north hand is
            change_x = palm[0] - GLOBAL_ORIGIN[0]
            change_y = GLOBAL_ORIGIN[1] - palm[1]
            degrees = math.degrees(math.atan2(change_x, change_y))
            if degrees < 0:
                degrees += 360

            if radius < OUTER_ANNULUS_START:
                # inner annulus
                button = int(degrees // 45)
                button_name = INNER_ANNULUS[button]

            else:
                # outer annulus
                button = int(degrees // 45)
                button_name = OUTER_ANNULUS[int(degrees // 45)]

                button = button + 8

        else:
            button = BUTTON_PLACEHOLDER

        held_button[hand] = button

        send = "B{}{}".format(hand, button)
        # B = button
        s.send(bytes(send, "UTF-8"))


def joystick_mode(hand, palm):
    if joy_origins[hand] == JOY_PLACEHOLDER:
        # origin not yet defined, define it
        joy_origins[hand] = palm
        # remove held button & set previous position to origin
        remove_button(hand)

    else:
        # determine distance between centre and current position
        change_x = palm[0] - joy_origins[hand][0]
        x = get_axis_value(change_x)

        change_y = joy_origins[hand][1] - palm[1]
        y = get_axis_value(change_y)

        send = "J{}{}y{}".format(hand, x, y) # J = joystick; y is delimiter
        s.send(bytes(send,"UTF-8"))


def remove_button(hand):
    # remove held button & update global variables back to defaults
    held_button[hand] = BUTTON_PLACEHOLDER
    previous_location[hand] = GLOBAL_ORIGIN
    send = "R{}".format(hand) # R = remove
    s.send(bytes(send,"UTF-8"))


def make_controller_input(landmarks, two_hands, w, h):

    frame_landmarks = get_frame_coords(landmarks, w, h)
    # stops error if part of hand out of frame
    if len(frame_landmarks) >= 20:
        open = check_if_hand_open(frame_landmarks)
        hand = check_left_right(frame_landmarks[:2])
        centre = get_palm_centre(frame_landmarks[0], frame_landmarks[5],
                             frame_landmarks[17])

        if not two_hands:
            # remove potential button held by missing hand
            other_hand = abs(hand - 1) # abs(1-0) = 0, abs(0-1) = 1
            remove_button(other_hand)

        if open:
            print("{} hand is open".format(hand))
            joystick_mode(hand, centre)

        else:
            print("{} hand is closed".format(hand))
            button_mode(hand, centre)

    else:
        print("Hand partially out of frame, can't find variables")


def get_frame_coords(landmarks, w, h):
    frame_landmarks = []

    for point in mp_hands.HandLandmark:
        normalised = landmarks.landmark[point]
        pixel_coord =\
        mp_drawing._normalized_to_pixel_coordinates(normalised.x, normalised.y,
                                                    w, h)

        try:
            frame_coord = ((pixel_coord[0] / w),
                          (pixel_coord[1] / h))

            frame_landmarks.append(frame_coord)

        # stop error from hand being partically out of frame. sometimes this is
        # not an issue, sometimes it is later on - this depends what landmarks
        # are missing so there's a length check in make_controller_input
        except TypeError:
            pass

    return frame_landmarks


def get_palm_centre(bottom, side_1, side_2):
    avg_x = (bottom[0] + side_1[0] + side_2[0])/3
    avg_y = (bottom[1] + side_1[1] + side_2[1])/3

    return (avg_x, avg_y)


def check_if_hand_open(landmarks):
    # 0 = index, 1 = middle,  2 = ring, 3 = pinky
    pip = [landmarks[6], landmarks[10],
            landmarks[14], landmarks[18]]
    dip = [landmarks[7], landmarks[11],
            landmarks[15], landmarks[19]]

    for finger in range(4):
        if pip[finger][1] < dip[finger][1]:
            return False

    return True


def check_left_right(landmarks):
    # 0th index = left; 1st index = right
    if landmarks[0][0] > landmarks[1][0]:
        return 1
    else:
        return 0


def line_distance(x, y):
    a = max(x) - min(x)
    b = max(y) - min(y)
    c2 = (a+b) ** 2
    c = math.sqrt(c2)
    return abs(c)


def get_axis_value(change):
    # gives output between -100 and 100
    value = 0
    if abs(change) < MAX_JOY_MOVEMENT:
        value = round((change * 4), 2) * 100
    else:
        if change < 0:
            value = -100

        else:
            value = 100
    return value


def get_overlay():
    _, frame = camera.read()
    img = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    # get overlay, resize to fit height of bg whilst matching aspect ratio
    overlay = cv2.imread("layout.png")
    overlay_h, overlay_w, _ = overlay.shape
    percentage = h / overlay_h
    new_overlay_w = int(overlay_w * percentage)
    new_size = (new_overlay_w, h)
    overlay = cv2.resize(overlay, new_size)

    # now add transparent border so that width is same as background
    x_shift = (w - new_overlay_w) // 2
    overlay = cv2.copyMakeBorder(overlay, 0, 0, x_shift, x_shift,
                                cv2.BORDER_CONSTANT, value=(0,0,0,1))

    return overlay


def main():
    s.connect((SERVER_MAC, PORT))

    overlay = get_overlay() # get overlay using 1st frame

    while camera.isOpened(): # run application
        _, frame = camera.read()

        img = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape

        img.flags.writeable = False
        results = hands.process(img)
        # draw hand annotations on the image for output.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        added_img = cv2.addWeighted(img, 0.5, overlay, 0.5, 0)

        if results.multi_hand_landmarks:
            two_hands = len(results.multi_hand_landmarks) == 2
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(added_img, hand_landmarks,
                                        mp_hands.HAND_CONNECTIONS)

                make_controller_input(hand_landmarks, two_hands,
                                     width, height)

        else:
            # no hands visible, remove button presses
            remove_button(0)
            remove_button(1)

        cv2.imshow('Controller', added_img)

        if cv2.waitKey(10) == 27:
            break # Esc key to close

    # end program
    hands.close() # mediapipe
    camera.release() # cv2
    cv2.destroyAllWindows() # cv2
    s.close() # bluetooth


main()