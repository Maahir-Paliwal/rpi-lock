from picamera2 import Picamera2
from facial_recognition import who_in_frame, format_frame
import time 
from gpiozero import LED
from gpiozero import Button 
import cv2
import signal 
import threading
import pickle



#Load the data from model.pickle for known_names
with open("model.pickle", "rb") as file:
    data = pickle.load(file)
known_names = data["names"]


led = LED(23)
buttonP = Button(24, pull_up=True, bounce_time=0.05)
lock = threading.Lock() 


def handle_press():
    #Only read this variable if it is not being written to
    print("button was pressed")

    with lock:
        signal = who_in_frame(current_names, known_names)
    
    #if the signal is true, then unlock, if not, then remain locked
    if (signal):
        led.on()
    else:
        led.off()

def button_loop():
    print("I have entered this thread")
    led.on()

    buttonP.when_pressed = handle_press

    signal.pause()




#start the thread for the button
threading.Thread(target=button_loop, daemon= True).start()


#start the camera up
cam = Picamera2()
cam.configure(cam.create_preview_configuration(main ={"size": (1920,1080), "format": 'XRGB8888'}))
cam.start()
time.sleep(2)




while True:
    
    frame = cam.capture_array()

    #get the names in the pic
    #This also updates global vars face_locations and face_encodings
    frame, names_in_picture = format_frame(frame)


    #Only write to this variable when it is not being read
    with lock:
        current_names = names_in_picture

    cv2.imshow('Facial Recognition Live Feed', frame)

    #Wait one millisecond and perform bitwise calculation for ASCII value
    key = cv2.waitKey(1) & 0xFF

    if (key ==ord('q')):
        break
    
    time.sleep(0.05)

#By breaking the loop we run this code here which closes everything
cv2.destroyAllWindows()
cam.stop()

