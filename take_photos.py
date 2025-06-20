#This file will be to automate the image taking process in case I would like to quickly
#give someone else access to the lock

import os
from datetime import datetime
from picamera2 import Picamera2
import time 
import cv2
import face_recognition




#Change this name to the person I want to add
NAME = "maahir"
SCALE_FACTOR = 1
BLUE = (0,255,0)
THICKNESS = 3

face_locations =[]

def create_folder(name): 

    #if ./dataset/name does not exist, create it 
    PERSON_PATH = f"dataset/{name}"
    if (not os.path.exists(PERSON_PATH)):
        os.makedirs(PERSON_PATH)

    return PERSON_PATH



def take_photos(name):
    folder = create_folder(NAME)

    #start the camera up
    cam = Picamera2()
    cam.configure(cam.create_preview_configuration(main ={"size": (640,480), "format": 'XRGB8888'}))
    cam.start()

    #allow for configurations to set up 
    time.sleep(2)

    num_photos = 0

    print(f"Initializing photo process for {name}")

    while True:
        #capture the frame from the picam 
        frame = cam.capture_array()

        cv2.imshow('Capture', frame)

        time.sleep(5)
        
        #resize the frame so that it can run quicker
        resized_frame = cv2.resize(frame, (0,0), fx=(1/SCALE_FACTOR),fy=(1/SCALE_FACTOR))
        rgb_resizedframe = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)


        face_locations = face_recognition.face_locations(rgb_resizedframe)
        (top, right, bottom, left) = face_locations

        top *= SCALE_FACTOR
        right *= SCALE_FACTOR
        bottom *= SCALE_FACTOR
        left *= SCALE_FACTOR

        
        #draw the rectangle but with 5px of padding
        cv2.rectangle(frame,(left - 5 ,top - 5), (bottom + 5, right +5), BLUE, THICKNESS)

        #Wait one millisecond and perform bitwise calculation for ASCII value
        key = cv2.waitKey(1) & 11111111

        if (key == ord(' ')):
            num_photos += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"

            #important that your face is not too far from the center of the screen or this
            # may cause undefined behaviour
            cropped_face = frame[(top-2):(bottom+2), (left-2):(right+2)]

            filepath = f"./{folder}/{filename}"

            cv2.imwrite(filepath, cropped_face)

            print(f"Photo {num_photos} saved to {filepath}")
        
        elif (key ==ord('q')):
            break 



    #clean
    cv2.destroyAllWindows()
    cam.stop()
    print(f"Photos taking complete. {num_photos} photos taken of {name}")


if __name__ == "__main__":
    take_photos(NAME)
