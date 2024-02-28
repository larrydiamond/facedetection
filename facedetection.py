import os
import sys
import face_recognition
from PIL import Image
import operator
import time
import threading
import pyttsx3
import cv2

print ("Face Detection starting")

BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"
names = []
encodings = []
labeledDirectory = sys.argv[1]
lock = threading.Lock()
face_location_model = 'hog'
number_of_times_to_upsample = 2

speech_engine = pyttsx3.init()

def load_threaded(file):
    image = face_recognition.load_image_file(os.path.join(labeledDirectory, file))
    face_locations = face_recognition.face_locations(img = image, number_of_times_to_upsample = number_of_times_to_upsample, model = face_location_model)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    for encoding in face_encodings:
        lock.acquire()
        names.append(file.split('_', 1)[0])
        encodings.append(encoding)
        lock.release()

def _recognize_face(unknown_encoding, loaded_encodings):
    """
    Given an unknown encoding and all known encodings, find the known
    encoding with the most matches.
    """
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )

    matches = {'Unknown': 0}

    loop = 0
    for match, name in zip(boolean_matches, loaded_encodings["names"]):
        if match:
            if name not in matches:
                matches[name] = 1
            else:
                matches[name] += 1
        loop = loop + 1

    print(str(matches))

    return max(matches.items(), key=operator.itemgetter(1))[0]

# Load labeled images
print ("Loading known images")
start_loading_images_time = time.time()

threads = []
for file in os.listdir(labeledDirectory):
    if file.endswith('.jpg'):
        load_threaded(file)
#        thread = threading.Thread(target=load_threaded, args=(file))
#        threads.append (thread)
#        thread.start()

#for thread in threads:
#    thread.join()

name_encodings = {"names": names, "encodings": encodings}

end_loading_images_time = time.time()
print (end_loading_images_time - start_loading_images_time)

print ("Loading camera image")

videoCaptureObject = cv2.VideoCapture(0)
lastSeen = {}

result = True
while(result):
    start_loading_camera_time = time.time()
    ret,unknownImage = videoCaptureObject.read()
    cv2.imwrite("NewPicture.jpg",unknownImage)

    input_face_locations = face_recognition.face_locations(img = unknownImage, number_of_times_to_upsample = number_of_times_to_upsample, model = face_location_model)
    input_face_encodings = face_recognition.face_encodings(unknownImage, input_face_locations)
    pilImage = Image.fromarray(unknownImage)

    print ("Results:")
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, name_encodings)
        if not name:
            name = "Unknown"

        if name not in lastSeen:
            print (name)
            speech_engine.say("We have detected " + name)
            lastSeen[name] = time.time()
        else:
            lastTime = lastSeen[name]
            currentTime = time.time()
            if (currentTime - lastTime) > 60:
                print (name)
                speech_engine.say("We have detected " + name)
            else:
                print ("already saw " + name)
            lastSeen[name] = time.time()

    end_recognition_time = time.time()
    print (end_recognition_time - start_loading_camera_time)
    speech_engine.runAndWait()

videoCaptureObject.release()




