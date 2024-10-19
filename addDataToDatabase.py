import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "https://attendance-system-fe3b4-default-rtdb.asia-southeast1.firebasedatabase.app/"

})

ref = db.reference('Students')

data = {
    "20010523100":{
        "Name" : "Nitin Mishra",
        "PRN" : "20010523100",
        "Subject" : "Deep Learning",
        "Class" : "AIML",
        "SEM" : "8",
        "Last_attendance" : "2024-04-22 00:41:35",
        "Total_attendance" : "8"
    },
    
    "20010523101":{
        "Name" : "Shivendra Yadav",
        "PRN" : "20010523101",
        "Subject" : "Deep Learning",
        "Class" : "AIML",
        "SEM" : "8",
        "Last_attendance" : "2024-04-22 00:41:35",
        "Total_attendance" : "8"
    },
    "20010523102":{
        "Name" : "Rupesh Jha",
        "PRN" : "20010523102",
        "Subject" : "Deep Learning",
        "Class" : "AIML",
        "SEM" : "8",
        "Last_attendance" : "2024-04-22 00:41:35",
        "Total_attendance" : "8"
    },
    "20010523103":{
        "Name" : "Gaurav Khalase",
        "PRN" : "20010523103",
        "Subject" : "Deep Learning",
        "Class" : "AIML",
        "SEM" : "8",
        "Last_attendance" : "2024-04-22 00:41:35",
        "Total_attendance" : "8"
    }
}


for key,value in data.items():
    ref.child(key).set(value)