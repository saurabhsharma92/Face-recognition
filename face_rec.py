import cv2
import easygui
import face_recognition

from homePage import homePage
#Use this if using Laptop's camera
video_capture = cv2.VideoCapture(0)
#Use this if you are using external camera
#video_capture = cv2.VideoCapture(1)
saurabh_image = face_recognition.load_image_file("Saurabh_Sharma.jpg")
saurabh_face_encoding = face_recognition.face_encodings(saurabh_image)[0]
brian_image = face_recognition.load_image_file("brian.jpeg")
brian_face_encoding = face_recognition.face_encodings(brian_image)[0]
#disha_image = face_recognition.load_image_file("disha.jpg")
#disha_face_encoding = face_recognition.face_encodings(disha_image)[0]
rupam_image = face_recognition.load_image_file("rupam.jpeg")
rupam_face_encoding = face_recognition.face_encodings(rupam_image)[0]
#sam_image = face_recognition.load_image_file("Sam.jpg")
#sam_face_encoding = face_recognition.face_encodings(sam_image)[0]

known_face_encodings = [
    saurabh_face_encoding,
    brian_face_encoding,
    rupam_face_encoding
]
known_face_names = [
    "Saurabh Sharma",
    "Brian Alessi",
    "Rupam",
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a maqtch for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    customerName=""
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        text_show = "Hi, " + name + " Welcome !!"
        customerName = name
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        y0, dy = 50, 2
        for i,line in enumerate(text_show.split('\n')):
            y = y0 + i * dy
            #cv2.putText(frame, line, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, line, (50, y), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)
    if(customerName in known_face_names):
        #msg = "Welcome " + format(name)
        #easygui.msgbox(text_show, title=customerName)
        homePage().createhomepage(customerName)
        break
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()

