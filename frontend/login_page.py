import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def login_action():
    username = username_var.get().strip()
    password = password_var.get().strip()

    if not username and not password:
        status_var.set("Username and Password are required!")
        return
    if not username:
        status_var.set("Username is required!")
        return
    if not password:
        status_var.set("Password is required!")
        return

    app.destroy()
    if "dr" in username:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "doctor_dashboard.py"), username])
    elif "pa" in username:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "patient_dashboard.py"), username, "", username, "", "", "", "", ""])

def signup_action():
    app.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "signup.py")])

app = ttk.Window(themename="darkly")
app.title("HOPIFY/Login")
app.geometry("400x500")
app.resizable(False, False)

frame = ttk.Frame(app, padding=20)
frame.pack(fill=BOTH, expand=True)

card = ttk.Labelframe(frame, text="Login", padding=15, bootstyle="info")
card.pack(fill=X, pady=10)

ttk.Label(card, text="HOPIFY", font=("Helvetica", 18, "bold"), bootstyle="light").pack()

ttk.Label(card, text="Username", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
username_var = tk.StringVar()
ttk.Entry(card, textvariable=username_var, font=("Helvetica", 12), bootstyle="info").pack(fill=X, ipady=6)

ttk.Label(card, text="Password", font=("Helvetica", 10), bootstyle="secondary").pack(anchor=W)
password_var = tk.StringVar()
ttk.Entry(card, textvariable=password_var, font=("Helvetica", 12), show="*", bootstyle="info").pack(fill=X, ipady=6)

status_var = tk.StringVar()
ttk.Label(frame, textvariable=status_var, bootstyle="danger").pack(pady=5)

ttk.Button(frame, text="Login", bootstyle="primary", command=login_action).pack(fill=X, ipady=8)
ttk.Button(frame, text="Sign Up", bootstyle="secondary-outline", command=signup_action).pack(fill=X, ipady=9, pady=5)

app.mainloop()