import csv
import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-fe3b4-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "attendance-system-fe3b4.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imageBackground = cv2.imread("Resources/background.png")

folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

file = open('encodedFile.p', 'rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownwithIds

modeType = 2
counter = 0
id = -1
imgStudent = []

# Dictionary to track whether attendance has been taken for each student
attendance_taken = {student_id: False for student_id in studentIds}
show_details_timer = 0  # Timer to control how long to show student details on the display

# Create a CSV file to store attendance
with open('attendance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['PRN', 'Name', 'Subject', 'Class', 'Semester', 'Attendance Time'])


def stop_program(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 427 <= x <= 686 and 124 <= y <= 183:  # Check if mouse click is within button coordinates
            exit(0)


cv2.namedWindow('Face recognition')
cv2.setMouseCallback('Face recognition', stop_program)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imageBackground[162:162 + 480, 55:55 + 640] = img
    imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imageBackground = cvzone.cornerRect(imageBackground, bbox, rt=0)
            id = studentIds[matchIndex]

            if not attendance_taken[id]:
                attendance_taken[id] = True

                # Get the data of students
                student_info = db.reference(f'Students/{id}').get()
                print(student_info)

                # Get the Image of the students
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update the date of attendance
                ref = db.reference(f'Students/{id}')
                ref.child('Last_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                # Set timer to show student details for 3 seconds
                show_details_timer = 90  # Assuming 30 frames per second

                # Write attendance to CSV file
                with open('attendance.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([id, student_info['Name'], student_info['Subject'], student_info['Class'],
                                     student_info['SEM'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    # Decrement timer
    if show_details_timer > 0:
        show_details_timer -= 1
    else:
        # Reset student details when timer expires
        modeType = 2
        counter = 0
        id = -1
        imgStudent = []

    if show_details_timer > 0:
        # Show student details on display
        classs = f"Class: {student_info['Class']}"
        prn = f"PRN: {id}"
        sub = f"Sub: {student_info['Subject']}"
        sem = f"Sem: {student_info['SEM']}"
        name = "Name: " + student_info['Name']
        (w, h), _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imageBackground, classs, (877, 531),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
        cv2.putText(imageBackground, prn, (877, 492),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
        cv2.putText(imageBackground, sub, (877, 561),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
        cv2.putText(imageBackground, sem, (877, 601),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
        cv2.putText(imageBackground, name, (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
        imageBackground[175:175 + 216, 909:909 + 216] = imgStudent

    # Display the button
    cv2.rectangle(imageBackground, (427, 124), (686, 183), (255, 0, 0), cv2.FILLED)
    cv2.putText(imageBackground, "STOP", (500, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Face recognition", imageBackground)
    cv2.waitKey(1)
