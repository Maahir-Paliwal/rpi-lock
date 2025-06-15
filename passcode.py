from gpiozero import Button
from gpiozero import LED
from signal import pause
from functools import partial
from time import sleep 
from fsm import handle_press


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


button_tuple = [("1", button1), ("2",button2), ("3",button3), ("4",button4),
            ("5",button5), ("6",button6), ("7",button7), ("8",button8), ("R",buttonR)]


current_state = "A"
def handle_press_wrapper(label):
    global current_state
    current_state = handle_press(label, current_state)



for label, button in button_tuple:
    
    #partial allows us to call the function and change the label
    button.when_pressed = partial(handle_press_wrapper, label)



pause()