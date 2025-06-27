import face_recognition 
import cv2
import pickle
from picamera2 import Picamera2
import numpy as np

SCALE_FACTOR = 4
THICKNESS = 3
face_locations = []
face_encodings = []

with open("model.pickle", "rb") as file:
    data = pickle.load(file)

known_face_encodings = data["encodings"]
known_names = data["names"]

def analyze_faces(frame):
    #we can keep these global since we never append to them
    #we keep changing the pointer but not appending, therefore no issues with storage
    global face_locations, face_encodings


    #resize the frame so that it can run quicker
    resized_frame = cv2.resize(frame, (0,0), fx=(1/SCALE_FACTOR),fy=(1/SCALE_FACTOR))
    rgb_resizedframe = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    #get all face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_resizedframe)
    face_encodings = face_recognition.face_encodings(rgb_resizedframe, face_locations, model='large')

    #names in picture will be of the same length of face_encodings and serves as a reference of who each encoding is
    names_in_picture = []

    for face_encoding in face_encodings:

        name = "unknown"
        #return a list of the same size with true/false values for matching
        matches_list = face_recognition.compare_faces(known_face_encodings, face_encoding)

        #return a list of distances to determine which has smallest
        faces_dist_array = face_recognition.face_distance(known_face_encodings, face_encoding)

        #find the smallest distance and return its index
        best_match_index = np.argmin(faces_dist_array)

        #if that smallest index was a match, then we can be sure it is a known person
        if matches_list[best_match_index]:
            name = known_names[best_match_index]
        
        #add the name
        names_in_picture.append(name)
    
    return names_in_picture 


def format_frame(frame):

    names_in_picture = analyze_faces(frame)

    for (top,right, bottom, left), name in zip(face_locations, names_in_picture):
        top *= SCALE_FACTOR
        right *= SCALE_FACTOR
        bottom *= SCALE_FACTOR
        left *= SCALE_FACTOR

        #Draw a box around the face
        cv2.rectangle(frame, (left,top), (right, bottom), (244,42,3), THICKNESS)

        #Draw their name as a label
        cv2.rectangle(frame, (left -3, top - 35), (right+3, top), (244, 42, 3), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    return frame, names_in_picture



def who_in_frame(names_in_picture, recognized_names):

    people_in_picture =[]
    for name in names_in_picture:
        if (name in recognized_names):
            people_in_picture.append(name)

    if len(people_in_picture) == 0:
        print("Unauthorized persons cannot open the door")

    else:
        for name in people_in_picture:
            print(f"Welcome {name}.")

    return len(people_in_picture) != 0

'''
#Load the data from model.pickle 
with open("model.pickle", "rb") as file:
    data = pickle.load(file)

known_face_encodings = data["encodings"]
known_names = data["names"]

#start the camera up
cam = Picamera2()
cam.configure(cam.create_preview_configuration(main ={"size": (1920,1080), "format": 'XRGB8888'}))
cam.start()

while True:
    frame = cam.capture_array()

    #get the names in the pic
    #This also updates global vars face_locations and face_encodings
    frame, names_in_picture = format_frame(frame)

    cv2.imshow('Facial Recognition Live Feed', frame)

    #Wait one millisecond and perform bitwise calculation for ASCII value
    key = cv2.waitKey(1) & 0xFF

    if (key ==ord('q')):
        break

# By breaking the loop we run this code here which closes everything
cv2.destroyAllWindows()
cam.stop()
'''





















