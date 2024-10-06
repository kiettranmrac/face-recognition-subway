import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import db, credentials, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-subway-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recognition-subway.appspot.com"
})

# importing customer images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
ids = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    ids.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def findEncodings(imagesList):
    encodeList = []

    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding starting...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, ids]
print("Encoding completed")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File saved")

