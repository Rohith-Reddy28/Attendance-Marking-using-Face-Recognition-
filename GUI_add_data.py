import tkinter as tk
from firebase_admin import credentials, db, initialize_app
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred , {
    'databaseURL' : "https://attendance-system-fe3b4-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Function to add data to Firebase
def add_data():
    prn = prn_entry.get()
    name = name_entry.get()
    subject = subject_entry.get()
    clas = class_entry.get()
    sem = sem_entry.get()
    
    default_last_attendance = "2024-04-22 00:41:35"  # Default value for Last_attendance
    
    data = {
        "Name": name,
        "PRN": prn,
        "Subject": subject,
        "Class": clas,
        "SEM": sem,
        "Last_attendance": default_last_attendance,
        "Total_attendance": "0"
    }
    
    ref = db.reference('Students')
    ref.child(prn).set(data)
    
    status_label.config(text="Data added successfully!")

# Create Tkinter window
window = tk.Tk()
window.title("Add Student Data")
window.geometry("640x480")  # Set window size

# PRN
prn_label = tk.Label(window, text="PRN:")
prn_label.grid(row=0, column=0, padx=5, pady=5)
prn_entry = tk.Entry(window)
prn_entry.grid(row=0, column=1, padx=5, pady=5)

# Name
name_label = tk.Label(window, text="Name:")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(window)
name_entry.grid(row=1, column=1, padx=5, pady=5)

# Subject
subject_label = tk.Label(window, text="Subject:")
subject_label.grid(row=2, column=0, padx=5, pady=5)
subject_entry = tk.Entry(window)
subject_entry.grid(row=2, column=1, padx=5, pady=5)

# Class
class_label = tk.Label(window, text="Class:")
class_label.grid(row=3, column=0, padx=5, pady=5)
class_entry = tk.Entry(window)
class_entry.grid(row=3, column=1, padx=5, pady=5)

# SEM
sem_label = tk.Label(window, text="SEM:")
sem_label.grid(row=4, column=0, padx=5, pady=5)
sem_entry = tk.Entry(window)
sem_entry.grid(row=4, column=1, padx=5, pady=5)

# Button to add data
add_button = tk.Button(window, text="Add Data", command=add_data)
add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Status label
status_label = tk.Label(window, text="")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
