import face_recognition
import cv2
from os import walk

peoples_names = []
face_encodings_array = []

def updateFiles():
    global peoples_names
    global face_encodings_array

    #known_people_path = "/home/giovanni/Documentos/ITQ/face_recognition/recognition/known_people"
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
        print(filename)
        #images.append(face_recognition.load_image_file("/home/giovanni/Documentos/ITQ/face_recognition/recognition/known_people/" + filename))
        images.append(face_recognition.load_image_file("/home/giovanni/Dropbox/Aplicaciones/SmartVilla/" + filename))
    face_encodings_array = []
    for image in images:
        face_encodings_array.append(face_recognition.face_encodings(image)[0])

    return peoples_names, face_encodings_array
def find():
    #if repeat == 1:
    #    peoples_names, face_encodings_array = updateFiles()
    #peoples_names, face_encodings_array = updateFiles()
    global peoples_names
    global face_encodings_array
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    video_capture = cv2.VideoCapture(0)

    # Grab a single frame of video
    try:
        ret, frame = video_capture.read()
    except Exception as e:
        return e
    # Resize frame of video to 1/4 size for faster face recognition processing
    try:
        if not frame:
            video_capture.release
            #return False
    except ValueError:
        small_frame = frame
    try:
        cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    except Exception as e:
        return e
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        if len(face_locations) == 0:
            return "NoOne"
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = "Unknown"
            i = 0
            for encoding in face_encodings_array:
                match = face_recognition.compare_faces([encoding], face_encoding, tolerance=0.5)
                if match[0]:
                    name = peoples_names[i]
                    return name
                    break
                else:
                    i += 1
            face_names.append(name)
    process_this_frame = not process_this_frame
    return name
