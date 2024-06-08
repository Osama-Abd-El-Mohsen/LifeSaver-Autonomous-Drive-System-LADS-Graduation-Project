import cv2
from datetime import datetime
from pub import *
import sys


face_cascade = cv2.CascadeClassifier("D:\Projects\Project 3\Code\Eye_Driver_RPI\haarcascade_frontalface_alt.xml")
eye_cascade = cv2.CascadeClassifier('D:\Projects\Project 3\Code\Eye_Driver_RPI/haarcascade_eye_tree_eyeglasses.xml')

current_time = ''
current_time2 = ''
last_eye_detection_time = ''
last_face_detection_time = ''
time_difference = ''
time_difference2 = ''
fase_found = False

state = 2 

last_face_detection_time = datetime.now()

# Function to detect eyes


def detect_eyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    return len(eyes)

# Function to detect if eyes are open or closed


def detect_closed_eyes(img):
    global current_time, time_difference, last_eye_detection_time, fase_found,state
    eyes_count = detect_eyes(img)
    
    if state == 2 and eyes_count == 0:
        last_eye_detection_time = datetime.now()
        state = 1


    if eyes_count == 0 and state == 1:
        current_time = datetime.now()
        time_difference = current_time - last_eye_detection_time
        print(time_difference.total_seconds())
        cv2.putText(img,str(time_difference.total_seconds()), (100,20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (125, 246, 55))
        if time_difference.total_seconds() >= 6:
            print('No eyes detected for 6 seconds. Sending message...')
            last_eye_detection_time = current_time
            publish_msg('1','esp32/sms_state')
            print('1 Puplised to esp32/sms_state')
            time.sleep(2)
            publish_msg('0','esp32/sms_state')
            print('0 Puplised to esp32/sms_state')
            sys.exit()
        return "Closed"

    else:
        print('0 Puplised to esp32/sms_state')
        publish_msg('0','esp32/sms_state')
        last_eye_detection_time = datetime.now()
        state = 2
        return "Open"


# Initialize camera
if sys.platform == 'linux':  # RPi camera
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
else:  # Laptop camera
    camera = cv2.VideoCapture(0)



while True : 
    if sys.platform == 'linux':  # RPi camera
        frame = camera.capture(rawCapture, format="bgr", use_video_port=True)
        image = frame.array
    else:  # Laptop camera
        ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop through each face and detect eyes
    if len(faces) != 0:
        last_face_detection_time = datetime.now()
        print('Face Found')
        for (x, y, w, h) in faces:
            fase_found = True
            roi = image[y:y+h, x:x+w]
            status = detect_closed_eyes(roi)
            cv2.putText(image, status, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        # current_time2 = datetime.now()
        # time_difference2 = current_time2 - last_face_detection_time
        # print(time_difference2.total_seconds())
        # if time_difference2.total_seconds() >= 60:
        #     print('No Face detected for 30 seconds. Sending message...')
        #     publish_msg('1','esp32/sms_state')
        #     last_face_detection_time = current_time2

        print('No Face Found')
        fase_found = False

    # Display the frame
    cv2.imshow('Eye Detection', image)


    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cv2.destroyAllWindows()
if sys.platform == 'linux':  # RPi camera
    camera.close()
else:  # Laptop camera
    camera.release()