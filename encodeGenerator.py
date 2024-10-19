
import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://attendance-system-fe3b4-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket' : "attendance-system-fe3b4.appspot.com"

})

# importing the student images

folderImagePath = "Images"
imagePathList = os.listdir(folderImagePath)
studentIds = []

studimgList = []
for path in imagePathList:
    studimgList.append(cv2.imread(os.path.join(folderImagePath, path)))
    studentIds.append(os.path.splitext(path)[0])


    fileName = f'{folderImagePath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)




def findEncodings(imagesList):
    encodedList = []

    for img in imagesList:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodedList.append(encode)

    return encodedList


print("Encoding Started...")


encodeListKnown = findEncodings(studimgList)
print(encodeListKnown)
encodeListKnownwithIds = [encodeListKnown ,  studentIds]
print("Encoding Ended...")


file = open("encodedFile.p" ,'wb')

pickle.dump(encodeListKnownwithIds , file)
file.close()
print("File generated")