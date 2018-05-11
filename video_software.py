import face_recognition
import cv2
from os import walk

peoples_names = []
face_encodings_array = []


def updateFiles():
    global peoples_names
    global face_encodings_array

    known_people_path = "/home/giovanni/Dropbox/Aplicaciones/SmartVilla"
    files = []
    for (dirpath, dirnames, filenames) in walk(known_people_path):
        files.extend(filenames)
        break

    try:
        files.remove(".dropbox")
    except ValueError:
        print ".dropbox already removed"

    print(files)

    peoples_names = []
    for names in files:
        peoples_names.append(names.split(".j")[0])
    print(peoples_names)
    images = []
    for filename in files:
        images.append(face_recognition.load_image_file(known_people_path + "/" + filename))
    face_encodings_array = []
    for image in images:
        face_encodings_array.append(face_recognition.face_encodings(image)[0])


def find():
    global peoples_names
    global face_encodings_array

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    video_capture = cv2.VideoCapture(0)
    tries = 0
    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            if len(face_locations) == 0:
                name = "NoOne"
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(face_encodings_array, face_encoding, tolerance=0.5)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = peoples_names[first_match_index]
                    return name

                #face_names.append(name)

        process_this_frame = not process_this_frame
        if tries == 500:
            return name
        tries += 1


    video_capture.release()
