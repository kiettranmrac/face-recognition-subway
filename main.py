import os
import pickle
from datetime import datetime
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import db, credentials, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-subway-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recognition-subway.appspot.com"
})

bucket = storage.bucket()

# define camera
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/Background.png')

# importing mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# load the encoding file
print("Loading encoded file...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, ids = encodeListKnownWithIds
print("Encode file loaded")

modeType = 0
counter = 0
id = -1
subway_fee = 1.5
wait_seconds = 30

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[143:143+480,40:40+640] = img
    imgBackground[143:143+480,723:723+250] = imgModeList[modeType]

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIdx = np.argmin(faceDis)
            if matches[matchIdx]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 40 + x1, 143 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = ids[matchIdx]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "loading", (275,400))
                    cv2.imshow("Face Recognition Subway", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # get data
                info = db.reference(f'Customers/{id}').get()

                # get image from storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgCustomer = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update data of funds
                datetimeObject = datetime.strptime(info['last-paid-time'],
                                                  "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                if secondsElapsed > wait_seconds:
                    ref = db.reference(f'Customers/{id}')
                    info['funds'] -= subway_fee
                    info['times-paid'] += 1
                    ref.child('funds').set(info['funds'])
                    ref.child('times-paid').set(info['times-paid'])
                    ref.child('last-paid-time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[143:143 + 480, 723:723 + 250] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[143:143 + 480, 723:723 + 250] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(info['funds']), (900, 565),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(imgBackground, str(id), (815,505),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 1)
                    (w, h), _ = cv2.getTextSize(info['name'], cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)
                    offset = (200-w)//2
                    cv2.putText(imgBackground, str(info['name']), (750+offset, 407),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
                    imgBackground[190:190+170,760:760+170] = imgCustomer

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    info = []
                    imgCustomer = []
                    imgBackground[143:143 + 480, 723:723 + 250] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    cv2.imshow("Face Recognition Subway", imgBackground)
    cv2.waitKey(1)