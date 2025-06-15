from gpiozero import LED

led = LED(23)

def handle_press(label, current_state):

    print("This is button " + label)
    match current_state:
        case "A":
            current_state = "B" if label == "6" else "A"
        
        case "B":
            current_state = "C" if label == "2" else "B" if label == "6" else "A"

        case "C":
            current_state = "D" if label == "2" else "B" if label == "6" else "A"

        case "D":
            current_state = "E" if label == "4" else "B" if label == "6" else "A"
        
        case "E":
            current_state = "F" if label == "4" else "B" if label == "6" else "A"
        
        case "F":
            current_state = "G" if label == "7" else "B" if label == "6" else "A"

            #short circuit
            current_state == "G" and led.on() 
        
        case "G":
            current_state = "A" if label == "R" else "G"

            current_state == "A" and led.off()

        #default case never reached 
        case _:
            print("default case")

    return current_state