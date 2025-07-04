# rpi-lock

# Goals
1. Create a lock with facial ID capabilities and passcode override
2. Utilize raspberry pi + breadboard + raspbpi camera

# Software used
1. Scripting will be done with python
    A. OpenCV for image display, real time video feed, and bounding boxes
    B. Face-recognition API to recognize faces in live video
    C. Os to control file flow
    D. Numpy for array use
    E. gpiozero to interface with pin logic

# Hardware used
1. Raspberry pi 5
2. Standard wiring (22-28AWG) wires for current control on breadboard and GPIO pins
3. Breadboard buttons to simulate pin numbers, facial recog button, and lock button
4. Solenoid latch + relay + 12V power source in order to simulate locking and unlocking
    A. 20 AWG wires for Solenoid logic because solenoid requires ~ 0.6A (too strong of current for regular wiring)

# How to use




