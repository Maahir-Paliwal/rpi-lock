from gpiozero import Button
from gpiozero import LED
from functools import partial
from fsm import handle_press
from facial_recognition import format_frame, who_in_frame
from picamera2 import Picamera2
import cv2
import threading
import signal 
import time 
import pickle



current_state = "A"
names_in_picture = []
current_names = []
names_lock = threading.Lock()


button1 = Button(26, pull_up=True, bounce_time=0.05)
button2 = Button(13, pull_up=True, bounce_time=0.05)
button3 = Button(6, pull_up=True, bounce_time=0.05)
button4 = Button(5, pull_up=True, bounce_time=0.05)
button5 = Button(22, pull_up=True, bounce_time=0.05)
button6 = Button(27, pull_up=True, bounce_time=0.05)
button7 = Button(17, pull_up=True, bounce_time=0.05)
button8 = Button(4, pull_up=True, bounce_time=0.05)
buttonR = Button(18, pull_up=True, bounce_time=0.05)
buttonP = Button(24, pull_up=True, bounce_time=0.05)

led = LED(23)


button_tuple = [("1", button1), ("2",button2), ("3",button3), ("4",button4),("5",button5),
                 ("6",button6), ("7",button7), ("8",button8), ("R",buttonR), ("P", buttonP)]



#Load the data from model.pickle for known_names
with open("model.pickle", "rb") as file:
    data = pickle.load(file)
known_names = data["names"]







def handle_press_wrapper(label):
    global current_state, current_names

    #if picture not taken 
    if (label != "P"):
        current_state, signal = handle_press(label, current_state)
    
    #if picture is taken
    else:

        #Only read this variable if it is not being written to
        with names_lock:
            signal = who_in_frame(current_names, known_names)
    
        #if granted access, manually change FSM to be in unlocked state 
        if (signal):
            current_state = "G"
    
    #if the signal is true, then unlock, if not, then remain locked
    if (signal):
        led.on()
    else:
        led.off()





#activate all the buttons to be listening
for label, button in button_tuple:
    #partial allows us to call the function and change the label
    button.when_pressed = partial(handle_press_wrapper, label)




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
    with names_lock:
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

time.pause()

