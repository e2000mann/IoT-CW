# up887818
# IOT Coursework - Creating IOT Application for Video Game Controller
# Main Code

# imports
import cv2
import mediapipe as mp

# subroutines
def button_mode():
    pass


def joystick_mode():
    pass


def hand_open(landmarks, side):
    fingers = get_fingers(landmarks)

    open = False

    for finger in fingers:
        for i in range(0,3):
            if finger[i].x() > finger[i+1].x():
                open = True

    if open:
        print("{} hand is open".format(side))
        joystick_mode()
    else:
        print("{} hand is closed".format(side))
        button_mode()


def get_fingers(landmarks):
    structuredLandmarks = []
    for j in range(42):
      if( j %2 == 1):
          structuredLandmarks.append({ 'x': landmarks[j - 1], 'y': landmarks[j] })

    first_finger = structuredLandmarks[5:8]
    second_finger = structuredLandmarks[9:12]
    third_finger = structuredLandmarks[13:16]
    fourth_finger = structuredLandmarks[17:20]
    fingers = [first_finger, second_finger, third_finger,
              fourth_finger]

    return structuredLandmarks


# main section
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(min_detection_confidence=0.5,
                               min_tracking_confidence=0.5)

camera = cv2.VideoCapture(0)

while camera.isOpened():
    ret, frame = camera.read();
    cv2.imshow("original", frame)

    img = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    img.flags.writeable = False
    results = holistic.process(img)
    # Draw the hand annotations on the image for output.
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if results.left_hand_landmarks:
        hand_landmarks = results.left_hand_landmarks
        connections = mp_holistic.HAND_CONNECTIONS
        mp_drawing.draw_landmarks(img, hand_landmarks, connections)
        hand_open(results.left_hand_landmarks, "left")

    if results.right_hand_landmarks:
        hand_landmarks = results.right_hand_landmarks
        connections = mp_holistic.HAND_CONNECTIONS
        mp_drawing.draw_landmarks(img, hand_landmarks, connections)
        hand_open(results.right_hand_landmarks, "right")

    cv2.imshow('MediaPipe holistic', img)

    if cv2.waitKey(10) == 27:
        # end program
        holistic.close()
        camera.release()
        cv2.destroyAllWindows()
