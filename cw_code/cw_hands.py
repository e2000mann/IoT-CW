# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Main Code

# imports
import cv2
import mediapipe as mp
import math

# global variables
# origins[0] is left, origins[1] is right
# frame is from (0, 0) bottom left to (1, 1) top right
# global origin is (0.5, 0.5)
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
    radius = line_distance(0.5, palm[0], 0.5, palm[1])
    radius = abs(radius)
    print(radius)
    if radius < 0.25:
        # neutral position
        pass
    else:
        # button needs to be pressed
        # check how many degrees from y axis hand is
        line_c = line_distance(0.5, palm[0], 0.5 + radius, palm[1])
        line_c = abs(line_c)
        # lines a and b are just radius (radius)
        cos_angle = (line_c ** 2) + (2 * radius ** 2) / (2 * radius ** 2)
        print(cos_angle)
        angle = math.degrees(math.acos(cos_angle))
        print(str(angle))

        if radius >= 0.25 and radius < 0.375:
            #inner annulus
            button = inner_annulus[0]
        else:
            # outer annulus
            button = outer_annulus[0]


def joystick_mode(landmarks, hand, centre):
    # if origin not yet defined, define it
    if origins[hand] == (-1, -1):
        origins[hand] = centre

    # else determine radius
    else:
        difference_x = origins[hand][0] + centre[0]
        difference_y = origins[hand][1] + centre[1]

    pass


def hand_details(landmarks):

    open = True

    # 0 = index, 1 = middle,  2 = ring, 3 = pinky
    mcps = [landmarks.landmark[5], landmarks.landmark[9],
            landmarks.landmark[13], landmarks.landmark[17]]
    tips = [landmarks.landmark[8], landmarks.landmark[12],
            landmarks.landmark[16], landmarks.landmark[20]]

    for finger in range(4):
        if mcps[finger].y < tips[finger].y:
            open = False
            break

    # hand 1 = right, hand 0 = left
    if mcps[0].x < mcps[1].x:
        hand = 1
    else:
        hand = 0

    centre = get_palm_centre(landmarks)

    if open:
        print("{} hand is open".format(hand))
        joystick_mode(landmarks, hand, centre)
    else:
        print("{} hand is closed".format(hand))
        button_mode(landmarks, hand, centre)


def get_palm_centre(landmarks):
    # 0 = bottom, 5 = edge 1, 17 = edge 2
    palm_bottom = landmarks.landmark[0]
    palm_side_1 = landmarks.landmark[5]
    palm_side_2 = landmarks.landmark[17]

    palm_avg_x = (palm_bottom.x + palm_side_1.x + palm_side_2.x)/3
    palm_avg_y = (palm_bottom.y + palm_side_1.y + palm_side_2.y)/3

    return (palm_avg_x, palm_avg_y)


def line_distance(x1, x2, y1, y2):
    a = x1 - x2
    b = y1 - y2
    c2 = (a+b) ** 2
    return math.sqrt(c2)


# main section
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

camera = cv2.VideoCapture(0)

while camera.isOpened():
    ret, frame = camera.read()
    cv2.imshow("original", frame)

    img = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    img.flags.writeable = False
    results = hands.process(img)
    # Draw the hand annotations on the image for output.
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks,
                                      mp_hands.HAND_CONNECTIONS)
            hand_details(hand_landmarks)

    cv2.imshow('MediaPipe Hands', img)

    if cv2.waitKey(10) == 27:
        # Esc key to close
        break

# end program
hands.close()
camera.release()
cv2.destroyAllWindows()
