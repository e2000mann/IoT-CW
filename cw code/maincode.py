# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Main Code

# imports
import cv2
import mediapipe as mp
import math

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
    radius = line_distance(0.5, palm[0], 0.5, palm[1])
    radius = abs(radius)
    if radius >= 0.25:
        # hand not in neutral position
        # button needs to be pressed
        # check how many degrees from y axis hand is
        line_c = line_distance(0.5, palm[0], 1, palm[1])
        line_c = abs(line_c)

        # lines a and b are just radius (radius)
        cos_angle = (line_c ** 2) / (2 * radius ** 2)
        print(cos_angle)
        angle = math.degrees(math.acos(cos_angle))
        print(str(angle))

        if radius < 0.375:
            # inner annulus
            button = inner_annulus[0]
        else:
            # outer annulus
            button = outer_annulus[0]


def joystick_mode(landmarks, hand, centre):
    # if origin not yet defined, define it
    if origins[hand] == (-1, -1):
        origins[hand] = centre

    # else determine distance between centre and current position
    else:
        distance = line_distance(origins[hand][0], centre[0],
                                 origins[hand][1], centre[1])


def hand_details(landmarks):
    frame_landmarks = get_frame_coords(landmarks)

    open = check_if_hand_open(frame_landmarks)
    hand = check_left_right(frame_landmarks[:2])
    centre = get_palm_centre(frame_landmarks[0], frame_landmarks[5],
                             frame_landmarks[17])

    if open:
        print("{} hand is open".format(hand))
        joystick_mode(frame_landmarks, hand, centre)
    else:
        print("{} hand is closed".format(hand))
        button_mode(frame_landmarks, hand, centre)


def get_frame_coords(landmarks):
    frame_landmarks = []

    for point in mp_hands.HandLandmark:
        normalised = landmarks.landmark[point]
        pixel_coord =\
        mp_drawing._normalized_to_pixel_coordinates(normalised.x, normalised.y,
                                                    image_width, image_height)

        frame_coord = ((pixel_coord[0] / image_width),
                       (pixel_coord[1] / image_height))

        frame_landmarks.append(frame_coord)

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
    image_height, image_width, _ = img.shape

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
