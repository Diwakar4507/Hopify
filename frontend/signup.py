import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def register_action():
    name     = name_var.get().strip()
    phone    = phn_var.get().strip()
    username = username_var.get().strip()
    password = password_var.get().strip()
    age      = age_var.get().strip()
    blood    = bg_var.get().strip()
    gender   = gender_var.get().strip()
    address  = address_var.get().strip()

    if not name:
        status_var.set("Name is required!")
        return
    if not phone:
        status_var.set("Phone number is required!")
        return
    if not phone.isdigit():
        status_var.set("Phone number must contain only digits!")
        return
    if not username:
        status_var.set("Username is required!")
        return
    if not password:
        status_var.set("Password is required!")
        return
    if len(password) < 6:
        status_var.set("Password must be at least 6 characters!")
        return
    if not age:
        status_var.set("Age is required!")
        return
    if not age.isdigit():
        status_var.set("Age must be a number!")
        return
    if not blood:
        status_var.set("Blood group is required!")
        return
    if not gender:
        status_var.set("Gender is required!")
        return
    if not address:
        status_var.set("Address is required!")
        return

    status_var.set("")
    if "dr" in username:
        app.destroy()
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "doctor_dashboard.py"), username])
    elif "pa" in username:
        app.destroy()
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "patient_dashboard.py"), username, "", username, "", "", "", "", ""])

def login_redirect():
    app.destroy()
    subprocess.Popen([sys.executable, "C:/Users/Pratik Fuyal/Desktop/Hopify/frontend/login_page.py"])

app = ttk.Window(themename="darkly")
app.title("HOPIFY/SignUp")
app.geometry("600x800")
app.resizable(False, False)

scroll = ScrolledFrame(app, autohide=True)
scroll.pack(fill=BOTH, expand=True)

frame = ttk.Frame(scroll, padding=20)
frame.pack(fill=BOTH, expand=True)

card = ttk.Labelframe(frame, text="Register", padding=15, bootstyle="info")
card.pack(fill=X, pady=10)

ttk.Label(card, text="HOPIFY", font=("Helvetica", 18, "bold"), bootstyle="light").pack()

ttk.Label(card, text="Name", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
name_var = tk.StringVar()
ttk.Entry(card, textvariable=name_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Phone Number", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
phn_var = tk.StringVar()
ttk.Entry(card, textvariable=phn_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Username", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
username_var = tk.StringVar()
ttk.Entry(card, textvariable=username_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Password", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
password_var = tk.StringVar()
ttk.Entry(card, textvariable=password_var, font=("Helvetica", 12), show="*", bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Age", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
age_var = tk.StringVar()
ttk.Entry(card, textvariable=age_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Blood Group", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
bg_var = tk.StringVar()
ttk.Entry(card, textvariable=bg_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Gender", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
gender_var = tk.StringVar()
ttk.Entry(card, textvariable=gender_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Address", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
address_var = tk.StringVar()
ttk.Entry(card, textvariable=address_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

status_var = tk.StringVar()
ttk.Label(frame, textvariable=status_var, bootstyle="danger").pack(pady=5)

ttk.Button(frame, text="Register", bootstyle="primary", command=register_action).pack(fill=X, ipady=8)
ttk.Button(frame, text="Back to Login", bootstyle="secondary-outline", command=login_redirect).pack(fill=X, ipady=8, pady=5)

app.mainloop()