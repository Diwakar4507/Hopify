"""
Hopify — Sign-Up Page
Separate tabs for Patient and Doctor registration.
Doctor tab includes NMC document upload.
"""

import tkinter as tk
from tkinter import ttk as stdttk, messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
import sys
import os

# ── Path setup ────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "backend"))
sys.path.insert(0, BACKEND_DIR)

import main as backend  # noqa: E402

# ── Colour palette ────────────────────────────────────────────────────────
BG_DARK    = "#0f1117"
BG_CARD    = "#1a1d2e"
BG_INPUT   = "#252840"
ACCENT     = "#6c63ff"
ACCENT2    = "#a78bfa"
TEXT_MAIN  = "#e2e8f0"
TEXT_SUB   = "#94a3b8"
TEXT_HINT  = "#64748b"
SUCCESS    = "#22d3a5"
DANGER     = "#f87171"
BORDER     = "#334155"
TAB_ACTIVE = "#252840"
DOC_BORDER = "#6c63ff"

FONT_LOGO  = ("Segoe UI", 20, "bold")
FONT_H1    = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_INPUT = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN   = ("Segoe UI", 11, "bold")

BLOOD_GROUPS = ["A+", "A−", "B+", "B−", "O+", "O−", "AB+", "AB−"]
GENDERS      = ["Male", "Female", "Other", "Prefer not to say"]
SPECIALIZATIONS = [
    "General Physician",
    "Cardiologist",
    "Dermatologist",
    "Neurologist",
    "Orthopedic Surgeon",
    "Pediatrician",
    "Psychiatrist",
    "Gynecologist",
    "Ophthalmologist",
    "ENT Specialist",
    "Urologist",
    "Oncologist",
    "Other",
]


# ─────────────────────────────────────────────────────────────────────────
#  Widget factory helpers
# ─────────────────────────────────────────────────────────────────────────

def _label(parent, text):
    """Plain label for optional fields."""
    row = tk.Frame(parent, bg=BG_CARD)
    row.pack(anchor=W, pady=(10, 0))
    tk.Label(row, text=text, font=FONT_LABEL, bg=BG_CARD,
             fg=TEXT_SUB).pack(side=LEFT)
    tk.Label(row, text=" (optional)", font=("Segoe UI", 8),
             bg=BG_CARD, fg=TEXT_HINT).pack(side=LEFT)


def _label_required(parent, text):
    """Label with a red asterisk indicating a required field."""
    row = tk.Frame(parent, bg=BG_CARD)
    row.pack(anchor=W, pady=(10, 0))
    tk.Label(row, text=text, font=FONT_LABEL, bg=BG_CARD,
             fg=TEXT_SUB).pack(side=LEFT)
    tk.Label(row, text=" *", font=FONT_LABEL, bg=BG_CARD,
             fg="#f87171").pack(side=LEFT)


def _entry(parent, var, show=""):
    """Styled text entry with focus ring animation."""
    outer = tk.Frame(parent, bg=BG_INPUT,
                     highlightbackground=BORDER, highlightthickness=1)
    outer.pack(fill=X, pady=(3, 0))
    e = tk.Entry(outer, textvariable=var, font=FONT_INPUT,
                 bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=ACCENT2,
                 relief="flat", show=show, bd=8)
    e.pack(fill=X)

    def on_in(ev):  outer.config(highlightbackground=ACCENT, highlightthickness=2)
    def on_out(ev): outer.config(highlightbackground=BORDER, highlightthickness=1)
    e.bind("<FocusIn>",  on_in)
    e.bind("<FocusOut>", on_out)
    return e


def _dropdown(parent, var, choices):
    """Styled Combobox dropdown."""
    style_name = "Dark.TCombobox"
    outer = tk.Frame(parent, bg=BG_INPUT,
                     highlightbackground=BORDER, highlightthickness=1)
    outer.pack(fill=X, pady=(3, 0))

    cb = stdttk.Combobox(outer, textvariable=var, values=choices,
                         font=FONT_INPUT, state="readonly")
    cb.pack(fill=X, ipady=5)

    # Style the combobox to match dark theme
    s = stdttk.Style()
    s.configure("Dark.TCombobox",
                 fieldbackground=BG_INPUT,
                 background=BG_INPUT,
                 foreground=TEXT_MAIN,
                 selectbackground=ACCENT,
                 selectforeground=TEXT_MAIN,
                 arrowcolor=ACCENT2,
                 borderwidth=0)
    s.map("Dark.TCombobox",
          fieldbackground=[("readonly", BG_INPUT)],
          foreground=[("readonly", TEXT_MAIN)],
          selectbackground=[("readonly", ACCENT)])

    cb.configure(style=style_name)

    def on_in(ev):  outer.config(highlightbackground=ACCENT, highlightthickness=2)
    def on_out(ev): outer.config(highlightbackground=BORDER, highlightthickness=1)
    cb.bind("<FocusIn>",  on_in)
    cb.bind("<FocusOut>", on_out)
    return cb


def _primary_btn(parent, text, command):
    btn = tk.Button(parent, text=text, font=FONT_BTN,
                    bg=ACCENT, fg="#ffffff", activebackground=ACCENT2,
                    activeforeground="#ffffff", relief="flat",
                    cursor="hand2", bd=0, padx=10, pady=11,
                    command=command)
    btn.pack(fill=X, pady=(14, 4))

    def on_in(e):  btn.config(bg=ACCENT2)
    def on_out(e): btn.config(bg=ACCENT)
    btn.bind("<Enter>", on_in)
    btn.bind("<Leave>", on_out)
    return btn


def _separator(parent):
    tk.Frame(parent, height=1, bg=BORDER).pack(fill=X, pady=8)


# ─────────────────────────────────────────────────────────────────────────
#  Business logic — Patient
# ─────────────────────────────────────────────────────────────────────────

def register_patient():
    name     = p_name_var.get().strip()
    phone    = p_phone_var.get().strip()
    username = p_username_var.get().strip()
    password = p_password_var.get().strip()
    age      = p_age_var.get().strip()
    blood    = p_blood_var.get().strip()
    gender   = p_gender_var.get().strip()
    address  = p_address_var.get().strip()

    # --- Required field validation ---
    errors = []
    if not name:     errors.append("Full name is required.")
    if not phone:    errors.append("Phone number is required.")
    elif not phone.isdigit(): errors.append("Phone must contain only digits.")
    if not username: errors.append("Username is required.")
    if not password: errors.append("Password is required.")
    elif len(password) < 6:  errors.append("Password must be ≥ 6 characters.")
    if not gender:   errors.append("Gender is required.")

    # --- Optional field format checks only (when provided) ---
    if age and not age.isdigit():
        errors.append("Age must be a number.")

    if errors:
        p_status_var.set(errors[0])
        p_status_lbl.config(fg=DANGER)
        return

    ok, msg = backend.register_patient(
        username, password, name, phone,
        int(age) if age else 0,
        blood, gender, address
    )
    if not ok:
        p_status_var.set(msg)
        p_status_lbl.config(fg=DANGER)
        return

    p_status_var.set("✓ " + msg)
    p_status_lbl.config(fg=SUCCESS)
    app.after(1200, lambda: _go_dashboard("patient", username))


# ─────────────────────────────────────────────────────────────────────────
#  Business logic — Doctor
# ─────────────────────────────────────────────────────────────────────────

def register_doctor():
    name    = d_name_var.get().strip()
    phone   = d_phone_var.get().strip()
    uname   = d_username_var.get().strip()
    passw   = d_password_var.get().strip()
    age     = d_age_var.get().strip()
    blood   = d_blood_var.get().strip()
    gender  = d_gender_var.get().strip()
    address = d_address_var.get().strip()
    spec    = d_spec_var.get().strip()
    nmc_doc = d_doc_path_var.get().strip()

    # --- Required field validation ---
    errors = []
    if not name:    errors.append("Full name is required.")
    if not phone:   errors.append("Phone number is required.")
    elif not phone.isdigit(): errors.append("Phone must contain only digits.")
    if not uname:   errors.append("Username is required.")
    if not passw:   errors.append("Password is required.")
    elif len(passw) < 6: errors.append("Password must be ≥ 6 characters.")
    if not gender:  errors.append("Gender is required.")
    if not spec:    errors.append("Specialization is required.")
    if not nmc_doc: errors.append("NMC document is required.")

    # --- Optional field format checks only (when provided) ---
    if age and not age.isdigit():
        errors.append("Age must be a number.")

    if errors:
        d_status_var.set(errors[0])
        d_status_lbl.config(fg=DANGER)
        return

    ok, msg = backend.register_doctor(
        uname, passw, name, phone,
        int(age) if age else 0,
        blood, gender, address, spec, nmc_doc
    )
    if not ok:
        d_status_var.set(msg)
        d_status_lbl.config(fg=DANGER)
        return

    d_status_var.set("✓ " + msg)
    d_status_lbl.config(fg=SUCCESS)
    app.after(1200, lambda: _go_dashboard("doctor", uname))


def browse_nmc_doc():
    """Open file dialog to pick NMC document."""
    filetypes = [
        ("All supported", "*.pdf *.jpg *.jpeg *.png *.tiff *.bmp"),
        ("PDF",  "*.pdf"),
        ("Image files", "*.jpg *.jpeg *.png *.tiff *.bmp"),
        ("All files",   "*.*"),
    ]
    path = filedialog.askopenfilename(
        title="Select NMC / Official Council Document",
        filetypes=filetypes,
    )
    if path:
        d_doc_path_var.set(path)
        short = os.path.basename(path)
        doc_name_lbl.config(text=short, fg=SUCCESS)
        d_status_var.set("")


def _go_dashboard(role: str, username: str):
    app.destroy()
    if role == "doctor":
        subprocess.Popen([sys.executable,
                          os.path.join(BASE_DIR, "doctor_dashboard.py"),
                          username])
    else:
        subprocess.Popen([sys.executable,
                          os.path.join(BASE_DIR, "patient_dashboard.py"),
                          username, "", username, "", "", "", "", ""])


def login_redirect():
    app.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "login_page.py")])


# ─────────────────────────────────────────────────────────────────────────
#  Build window
# ─────────────────────────────────────────────────────────────────────────

app = ttk.Window(themename="darkly")
app.title("Hopify — Sign Up")
app.geometry("520x780")
app.resizable(False, True)
app.configure(bg=BG_DARK)

# ── Header ────────────────────────────────────────────────────────────────
header = tk.Frame(app, bg=BG_DARK)
header.pack(fill=X, padx=30, pady=(22, 0))

tk.Label(header, text="HOPIFY", font=FONT_LOGO,
         bg=BG_DARK, fg=TEXT_MAIN).pack()
tk.Label(header, text="Create your account",
         font=FONT_SMALL, bg=BG_DARK, fg=TEXT_HINT).pack()

# ── Tab switcher ──────────────────────────────────────────────────────────
tab_row = tk.Frame(app, bg=BG_DARK)
tab_row.pack(fill=X, padx=30, pady=(16, 0))

# We build a manual tab bar so it looks premium on the dark bg.
patient_tab_btn = tk.Button(tab_row, text="  Patient  ", font=FONT_BTN,
                             relief="flat", cursor="hand2", bd=0,
                             pady=8, bg=ACCENT, fg="#ffffff")
patient_tab_btn.pack(side=LEFT, fill=X, expand=True)

doctor_tab_btn  = tk.Button(tab_row, text="  Doctor  ", font=FONT_BTN,
                             relief="flat", cursor="hand2", bd=0,
                             pady=8, bg=BG_CARD, fg=TEXT_SUB)
doctor_tab_btn.pack(side=LEFT, fill=X, expand=True)

# ── Scrollable card area ──────────────────────────────────────────────────
canvas_frame = tk.Frame(app, bg=BG_DARK)
canvas_frame.pack(fill=BOTH, expand=True, padx=30, pady=10)

canvas = tk.Canvas(canvas_frame, bg=BG_DARK, bd=0,
                   highlightthickness=0)
scrollbar = tk.Scrollbar(canvas_frame, orient=VERTICAL,
                          command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

inner_frame = tk.Frame(canvas, bg=BG_DARK)
canvas_window = canvas.create_window((0, 0), window=inner_frame,
                                      anchor=NW)


def _on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_window, width=canvas.winfo_width())


inner_frame.bind("<Configure>", _on_configure)
canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(canvas_window,
                                        width=e.width))

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ─────────────────────────────────────────────────────────────────────────
#  Patient form
# ─────────────────────────────────────────────────────────────────────────

patient_card = tk.Frame(inner_frame, bg=BG_CARD, bd=0,
                         highlightbackground=BORDER, highlightthickness=1)
patient_card.pack(fill=X, pady=(0, 10))

p_inner = tk.Frame(patient_card, bg=BG_CARD, padx=22, pady=18)
p_inner.pack(fill=BOTH)

tk.Label(p_inner, text="Patient Registration", font=FONT_H1,
         bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=W)
tk.Label(p_inner, text="Fill in your personal details below",
         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_SUB).pack(anchor=W, pady=(2, 8))

# Fields
p_name_var     = tk.StringVar()
p_phone_var    = tk.StringVar()
p_username_var = tk.StringVar()
p_password_var = tk.StringVar()
p_age_var      = tk.StringVar()
p_blood_var    = tk.StringVar()
p_gender_var   = tk.StringVar()
p_address_var  = tk.StringVar()

_label_required(p_inner, "FULL NAME");     _entry(p_inner, p_name_var)
_label_required(p_inner, "PHONE NUMBER");  _entry(p_inner, p_phone_var)
_label_required(p_inner, "USERNAME");      _entry(p_inner, p_username_var)
_label_required(p_inner, "PASSWORD");      _entry(p_inner, p_password_var, show="*")
_label(p_inner, "AGE");                    _entry(p_inner, p_age_var)
_label(p_inner, "BLOOD GROUP");            _dropdown(p_inner, p_blood_var, BLOOD_GROUPS)
_label_required(p_inner, "GENDER");        _dropdown(p_inner, p_gender_var, GENDERS)
_label(p_inner, "ADDRESS");                _entry(p_inner, p_address_var)

p_status_var = tk.StringVar()
p_status_lbl = tk.Label(p_inner, textvariable=p_status_var,
                          font=FONT_SMALL, bg=BG_CARD, fg=DANGER,
                          wraplength=430, justify=LEFT)
p_status_lbl.pack(anchor=W, pady=(8, 0))

_primary_btn(p_inner, "CREATE PATIENT ACCOUNT", register_patient)

# ─────────────────────────────────────────────────────────────────────────
#  Doctor form
# ─────────────────────────────────────────────────────────────────────────

doctor_card = tk.Frame(inner_frame, bg=BG_CARD, bd=0,
                        highlightbackground=BORDER, highlightthickness=1)

d_inner = tk.Frame(doctor_card, bg=BG_CARD, padx=22, pady=18)
d_inner.pack(fill=BOTH)

tk.Label(d_inner, text="Doctor Registration", font=FONT_H1,
         bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=W)
tk.Label(d_inner, text="Fill in your professional details below",
         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_SUB).pack(anchor=W, pady=(2, 8))

d_name_var     = tk.StringVar()
d_phone_var    = tk.StringVar()
d_username_var = tk.StringVar()
d_password_var = tk.StringVar()
d_age_var      = tk.StringVar()
d_blood_var    = tk.StringVar()
d_gender_var   = tk.StringVar()
d_address_var  = tk.StringVar()
d_spec_var     = tk.StringVar()
d_doc_path_var = tk.StringVar()

_label_required(d_inner, "FULL NAME");         _entry(d_inner, d_name_var)
_label_required(d_inner, "PHONE NUMBER");      _entry(d_inner, d_phone_var)
_label_required(d_inner, "USERNAME");          _entry(d_inner, d_username_var)
_label_required(d_inner, "PASSWORD");          _entry(d_inner, d_password_var, show="*")
_label(d_inner, "AGE");                        _entry(d_inner, d_age_var)
_label(d_inner, "BLOOD GROUP");                _dropdown(d_inner, d_blood_var, BLOOD_GROUPS)
_label_required(d_inner, "GENDER");            _dropdown(d_inner, d_gender_var, GENDERS)
_label(d_inner, "ADDRESS");                    _entry(d_inner, d_address_var)
_label_required(d_inner, "SPECIALIZATION");    _dropdown(d_inner, d_spec_var, SPECIALIZATIONS)

# ── NMC Document upload ───────────────────────────────────────────────────
_label_required(d_inner, "NMC / OFFICIAL COUNCIL DOCUMENT")

doc_area = tk.Frame(d_inner, bg=BG_CARD,
                    highlightbackground=DOC_BORDER, highlightthickness=1,
                    pady=14)
doc_area.pack(fill=X, pady=(3, 0))

tk.Label(doc_area,
         text="Upload your Nepal Medical Council registration document",
         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_SUB,
         justify=CENTER).pack(pady=(8, 6))

doc_name_lbl = tk.Label(doc_area, text="No file selected",
                          font=FONT_SMALL, bg=BG_CARD, fg=TEXT_HINT)
doc_name_lbl.pack(pady=(0, 6))

browse_btn = tk.Button(doc_area, text="Browse File",
                        font=("Segoe UI", 10, "bold"),
                        bg=BG_INPUT, fg=ACCENT2,
                        activebackground=ACCENT, activeforeground="#fff",
                        relief="flat", cursor="hand2", bd=0,
                        padx=16, pady=7, command=browse_nmc_doc)
browse_btn.pack()

tk.Label(doc_area,
         text="Accepted: PDF, JPG, PNG, TIFF",
         font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_HINT).pack(pady=(6, 0))

# status + register button
d_status_var = tk.StringVar()
d_status_lbl = tk.Label(d_inner, textvariable=d_status_var,
                          font=FONT_SMALL, bg=BG_CARD, fg=DANGER,
                          wraplength=430, justify=LEFT)
d_status_lbl.pack(anchor=W, pady=(8, 0))

_primary_btn(d_inner, "CREATE DOCTOR ACCOUNT", register_doctor)

# ── Footer ────────────────────────────────────────────────────────────────
footer = tk.Frame(app, bg=BG_DARK)
footer.pack(fill=X, padx=30, pady=(0, 12))

tk.Label(footer, text="Already have an account? ",
         font=FONT_SMALL, bg=BG_DARK, fg=TEXT_SUB).pack(side=LEFT)
login_lbl = tk.Label(footer, text="Login",
                      font=(FONT_SMALL[0], FONT_SMALL[1], "underline"),
                      bg=BG_DARK, fg=ACCENT2, cursor="hand2")
login_lbl.pack(side=LEFT)
login_lbl.bind("<Button-1>", lambda e: login_redirect())

# ─────────────────────────────────────────────────────────────────────────
#  Tab switching logic
# ─────────────────────────────────────────────────────────────────────────

def show_patient():
    doctor_card.pack_forget()
    patient_card.pack(fill=X, pady=(0, 10))
    patient_tab_btn.config(bg=ACCENT, fg="#ffffff")
    doctor_tab_btn.config(bg=BG_CARD, fg=TEXT_SUB)
    canvas.yview_moveto(0)


def show_doctor():
    patient_card.pack_forget()
    doctor_card.pack(fill=X, pady=(0, 10))
    doctor_tab_btn.config(bg=ACCENT, fg="#ffffff")
    patient_tab_btn.config(bg=BG_CARD, fg=TEXT_SUB)
    canvas.yview_moveto(0)


patient_tab_btn.config(command=show_patient)
doctor_tab_btn.config(command=show_doctor)

# Start on patient tab
show_patient()

app.mainloop()