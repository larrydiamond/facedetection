import os
import sys
import face_recognition
from PIL import Image, ImageDraw
import operator
import threading

print ("Face Detection starting")

model = "hog"
BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"
names = []
encodings = []
labeledDirectory = sys.argv[1]
unknownImageLocation = sys.argv[2]

def _recognize_face(unknown_encoding, loaded_encodings):
    """
    Given an unknown encoding and all known encodings, find the known
    encoding with the most matches.
    """
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )

    matches = {'unknown': 1}

    loop = 0
    for match, name in zip(boolean_matches, loaded_encodings["names"]):
        if match:
            if not name in matches:
                matches[name] = 1
            else:
                matches[name] += 1
        loop = loop + 1

    return max(matches.items(), key=operator.itemgetter(1))[0]

def _display_face(draw, bounding_box, name):
    """
    Draws bounding boxes around faces, a caption area, and text captions.
    """
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=BOUNDING_BOX_COLOR,
        outline=BOUNDING_BOX_COLOR,
    )
    draw.text(
        (text_left, text_top),
        name,
        fill=TEXT_COLOR,
    )

# Load labeled images
print ("Loading known images")

for file in os.listdir(labeledDirectory):
    if file.endswith('.jpg'):
        image = face_recognition.load_image_file(os.path.join(labeledDirectory, file))
        face_locations = face_recognition.face_locations(image, model = model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for encoding in face_encodings:
            names.append(file.split('_', 1)[0])
            encodings.append(encoding)

name_encodings = {"names": names, "encodings": encodings}

# load unknown image to compare
print ("Loading unknown image")

unknownImage = face_recognition.load_image_file(unknownImageLocation)
input_face_locations = face_recognition.face_locations(
    unknownImage, model=model
)
input_face_encodings = face_recognition.face_encodings(
    unknownImage, input_face_locations
)
pilImage = Image.fromarray(unknownImage)
draw = ImageDraw.Draw(pilImage)

for bounding_box, unknown_encoding in zip(
    input_face_locations, input_face_encodings
):
    name = _recognize_face(unknown_encoding, name_encodings)
    if not name:
        name = "Unknown"
    _display_face(draw, bounding_box, name)
    print (name)







