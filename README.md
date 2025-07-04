# rpi-lock



# Goals
1. Create a lock with facial ID capabilities and passcode override
2. Utilize raspberry pi + breadboard + raspbpi camera
3. Leverage a finite state machine (Mealy FSM) to effectively handle loicking and unlocking logic



# Software used
1. Scripting done with python
    A. OpenCV for image display, real time video feed, and bounding boxes
    B. Face-recognition API to recognize faces in live video
    C. Os to control file flow
    D. Numpy for array use
    E. gpiozero to interface with pin logic
2. Environment handled with venv 
3. Github for source control



# Hardware used
1. Raspberry pi 5
2. Standard wiring (22-28AWG) wires for current control on breadboard and GPIO pins
3. Breadboard buttons to simulate pin numbers, facial recog button, and lock button
4. Solenoid latch + relay + 12V power source in order to simulate locking and unlocking
    A. 20 AWG wires for Solenoid logic because solenoid requires ~ 0.6A (too strong of current for regular wiring)



# Logic and Workflow
take_photos.py -> model_training.py -> passcode.py

1. take_photos.py:
    - Takes images of the user's face and automatically creates a folder (simulating a dataset) for a model to be trained on
    - Leverages facial-recognition to identify faces in live time and extracts only pictures of faces

2. model_training.py
    - trains a model to recognize all faces in the dataset
    - turns each face into its own encoding 

3. passcode.py
    - Compares all known encodings in a dataset to the face of the user who wants to enter (logic handled in facial_recognition.py)
    - Calls fsm.py for state machine logic for passcode



# How to use
1. Pip install the requirements.txt document 

2. take_photos.py
    A. modify the name on line 13 to be the name of the person's face you want recognized
    B. run the script (python3 ./take_photos.py in your terminal)
    C. When a bounding box has surrounded your face, take a photo by pressing SPACE. After 5-10 photos are taken, press 'q' to quit.

3. model_training.py
    A. run the script (python3 ./model_training.py)

4. passcode.py
    A. Run the script (python3 ./passcode.py)
    B. Interface with the hardware and observe lock functionality!








