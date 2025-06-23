
def handle_press(label, current_state):

    print("This is button " + label)
    match current_state:
        case "A":
            current_state = "B" if label == "6" else "A"
            signal = False
        
        case "B":
            current_state = "C" if label == "2" else "B" if label == "6" else "A"
            signal = False

        case "C":
            current_state = "D" if label == "2" else "B" if label == "6" else "A"
            signal = False

        case "D":
            current_state = "E" if label == "4" else "B" if label == "6" else "A"
            signal = False
        
        case "E":
            current_state = "F" if label == "4" else "B" if label == "6" else "A"
            signal = False
        
        case "F":
            current_state = "G" if label == "7" else "B" if label == "6" else "A"

            #change the return value if we are in final state
            signal = True if current_state == "G" else False
        
        case "G":
            current_state = "A" if label == "R" else "G"

            
            signal = False if current_state == "A" else True

        #default case never reached 
        case _:
            print("default case")

    return current_state, signal