# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Main Code

# algorithm imports
import cv2
import mediapipe as mp
import math

# communication imports
import socket
import subprocess

# global variables
# origins[0] is left, origins[1] is right
origins = [(-1, -1), (-1, -1)]

inner_annulus = ["TRIANGLE", "RIGHT", "CIRCLE", "DOWN",
                 "CROSS", "LEFT", "SQUARE", "UP"]
outer_annulus = ["OPTIONS", "R2", "R1", "PS",
                 "TOUCHPAD", "L1", "L2", "SHARE"]


# subroutines
def button_mode(landmarks, hand, palm):
    # clear origin from joystick mode
    origins[hand] = (-1, -1)

    # check hand's radius (distance) from global origin
    radius = line_distance([0.5, palm[0]], [0.5, palm[1]])
    print(radius)

    if radius >= 0.25:
        # check how many degrees from north hand is
        change_x = palm[0] - 0.5
        change_y = 0.5 - palm[1]
        degrees = math.degrees(math.atan2(change_x, change_y))
        if degrees < 0:
            degrees += 360
        print(degrees)

        if radius < 0.375:
            # inner annulus
            button = int(degrees // 45)
            button_name = inner_annulus[button]

        else:
            # outer annulus
            button = int(degrees // 45)
            button_name = outer_annulus[int(degrees // 45)]

            button = button + 8

    else:
        button = 17

    # send B to show it's button output
    s.send(bytes("B", 'UTF-8'))
    # send hand value
    s.send(bytes(str(hand), "UTF-8"))
    # send button value from 1-16
    s.send(bytes(str(button), 'UTF-8'))


def joystick_mode(landmarks, hand, palm):
    # if origin not yet defined, define it
    if origins[hand] == (-1, -1):
        origins[hand] = palm

    # else determine distance between centre and current position
    else:
        change_x = palm[0] - origins[hand][0]
        x = get_axis_value(change_x)

        change_y = origins[hand][1] - palm[1]
        y = get_axis_value(change_y)

        print("x: {} y: {}".format(x,y))

        # send J to show it's joystick output
        s.send(bytes("J", "UTF-8"))
        # send hand value
        s.send(bytes(str(hand), "UTF-8"))
        # send x
        s.send(bytes(str(x), "UTF-8"))
        # send y
        s.send(bytes(str(y), "UTF-8"))


def hand_details(landmarks):
    frame_landmarks = get_frame_coords(landmarks)
    # stops error if part of hand out of frame
    if len(frame_landmarks) >= 20:
        open = check_if_hand_open(frame_landmarks)
        hand = check_left_right(frame_landmarks[:2])
        centre = get_palm_centre(frame_landmarks[0], frame_landmarks[5],
                             frame_landmarks[17])

        if open:
            print("{} hand is open".format(hand))
            return joystick_mode(frame_landmarks, hand, centre)

        else:
            print("{} hand is closed".format(hand))
            return button_mode(frame_landmarks, hand, centre)

    else:
        print("Hand partially out of frame, can't find variables")
        return ""


def get_frame_coords(landmarks):
    frame_landmarks = []

    for point in mp_hands.HandLandmark:
        normalised = landmarks.landmark[point]
        pixel_coord =\
        mp_drawing._normalized_to_pixel_coordinates(normalised.x, normalised.y,
                                                    image_width, image_height)

        try:
            frame_coord = ((pixel_coord[0] / image_width),
                          (pixel_coord[1] / image_height))

            frame_landmarks.append(frame_coord)

        # stop error from hand being partically out of frame. sometimes this
        # is not an issue, sometimes it is later on - this depends what
        # landmarks are missing - hence there's a length check in hand_details
        except TypeError:
            pass

    return frame_landmarks


def get_palm_centre(bottom, side_1, side_2):
    # 0 = bottom, 5 = edge 1, 17 = edge 2
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
    # hand 1 = right, hand 0 = left
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
    value = 0
    if -0.25 < change and change < 0.25:
        value = change * 4
    else:
        if change < 0:
            value = -1

        else:
            value = 1

    return value


def get_overlay(bg_width, bg_height):
    # get overlay, resize to fit height of background whilst matching
    # aspect ratio
    overlay = cv2.imread("layout.png")
    image_height, image_width, _ = overlay.shape
    percentage = bg_height / image_height
    new_image_width = int(image_width * percentage)
    new_size = (new_image_width, bg_height)
    overlay = cv2.resize(overlay, new_size)

    # now add transparent border so that width is same as background
    x_shift = (bg_width - new_image_width) // 2
    overlay = cv2.copyMakeBorder(overlay, 0, 0, x_shift, x_shift,
                                cv2.BORDER_CONSTANT, value=(0,0,0,1))

    return overlay

# main section
# set up bluetooth
server_mac = "00:19:10:09:27:26"
port = 1
passkey = "1234"

# necessary as hc-06 by default needs passkey to connect
# kill any "bluetooth-agent" process that is already running, then start
# a new "bluetooth-agent" process which includes passkey
# subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)
# status = subprocess.call("bluetooth-agent " + passkey + " &",shell=True)

s = socket.socket(socket.AF_BLUETOOTH,
                 socket.SOCK_STREAM,
                 socket.BTPROTO_RFCOMM)
s.connect((server_mac, port))

# set up cv2 & mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.75,
                       min_tracking_confidence=0.5)
camera = cv2.VideoCapture(0)

# run application
while camera.isOpened():
    ret, frame = camera.read()

    img = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = img.shape

    img.flags.writeable = False
    results = hands.process(img)
    # Draw the hand annotations on the image for output.
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    overlay = get_overlay(image_width, image_height)

    added_img = cv2.addWeighted(img, 0.5, overlay, 0.5, 0)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(added_img, hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS)

            hand_details(hand_landmarks)

    cv2.imshow('Controller', added_img)

    if cv2.waitKey(10) == 27:
        # Esc key to close
        break

# end program
hands.close() # mediapipe
camera.release() # cv2
cv2.destroyAllWindows() # cv2
s.close() # bluetooth
