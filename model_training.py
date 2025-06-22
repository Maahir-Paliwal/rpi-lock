import os
import pickle
import face_recognition

known_encodings = []
known_names = []

#ugly time complexity, maybe there is a way to do better
for name in os.listdir("./dataset/"):

    index = 1

    file_path = f"./dataset/{name}"
    print(file_path)
    for picture in os.listdir(file_path):
        print(f"reading picture {index}/{len(os.listdir(file_path))} of {name} ...")

        image = face_recognition.load_image_file(file=f"{file_path}/{picture}",mode='RGB')


        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(face_image=image, known_face_locations=face_locations, model='large')

        known_names.append(name)

        #there should only be 1 face in the picture
        known_encodings.append(face_encodings[0])

        index += 1

print("finishing encodings")

file_data = {"names":known_names, "encodings": known_encodings}

with open("model.pickle", "wb") as file:
    pickle.dump(file_data, file)









