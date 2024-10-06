import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-subway-default-rtdb.firebaseio.com/"
})

ref = db.reference("Customers")

data = {
    "6132126":
        {
            "name": "Minh Anh",
            "dob": "2004-05-04",
            "sex": "Female",
            "last-paid-time": "2024-10-06 04:45:35",
            "funds": 15,
            "times-paid": 10
        },
    "6132433":
        {
            "name": "Bob Iuliano",
            "dob": "1832-01-01",
            "sex": "Male",
            "last-paid-time": "2024-10-05 12:34:41",
            "funds": 3.5,
            "times-paid": 1
        },
    "6132987":
        {
            "name": "Kiet Tran",
            "dob": "2004-09-13",
            "sex": "Male",
            "last-paid-time": "2024-10-04 19:41:35",
            "funds": 17,
            "times-paid": 2
        }
}

for key, value in data.items():
    ref.child(key).set(value)