from gpiozero import Button
from gpiozero import LED
from signal import pause
from functools import partial
from time import sleep 


#Only 9 buttons b/c saving one for picture
button1 = Button(26, pull_up=True, bounce_time=0.05)
button2 = Button(13, pull_up=True, bounce_time=0.05)
button3 = Button(6, pull_up=True, bounce_time=0.05)
button4 = Button(5, pull_up=True, bounce_time=0.05)
button5 = Button(22, pull_up=True, bounce_time=0.05)
button6 = Button(27, pull_up=True, bounce_time=0.05)
button7 = Button(17, pull_up=True, bounce_time=0.05)
button8 = Button(4, pull_up=True, bounce_time=0.05)
buttonR = Button(18, pull_up=True, bounce_time=0.05)

led = LED(23)

button_tuple = [("1", button1), ("2",button2), ("3",button3), ("4",button4),
            ("5",button5), ("6",button6), ("7",button7), ("8",button8), ("R",buttonR)]

current_state = "A"


#mealy FSM to detect '622447'
def handle_press(label):

    global current_state

    print("This is button " + label)
    match current_state:
        case "A":
            current_state = "B" if label == "6" else "A"

            return
        
        case "B":
            current_state = "C" if label == "2" else "B" if label == "6" else "A"
            return

        case "C":
            current_state = "D" if label == "2" else "B" if label == "6" else "A"
            return

        case "D":
            current_state = "E" if label == "4" else "B" if label == "6" else "A"
            return
        
        case "E":
            current_state = "F" if label == "4" else "B" if label == "6" else "A"
            return 
        
        case "F":
            current_state = "G" if label == "7" else "B" if label == "6" else "A"

            #short circuit
            current_state == "G" and led.on() 

            return
        
        case "G":
            current_state = "A" if label == "R" else "G"

            current_state == "A" and led.off()
        
            return

        #default case never reached 
        case _:
            print("default case")



for label, button in button_tuple:
    
    #partial allows us to call the function and change the label
    button.when_pressed = partial(handle_press, label)



pause()