"""
Hopify — Login Page
A polished tkinter / ttkbootstrap login screen.
"""

import tkinter as tk
from tkinter import messagebox
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

FONT_LOGO  = ("Segoe UI", 22, "bold")
FONT_H1    = ("Segoe UI", 15, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_INPUT = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_BTN   = ("Segoe UI", 11, "bold")


# ── Helpers ───────────────────────────────────────────────────────────────

def _make_entry(parent, var, placeholder="", show=""):
    """Styled entry with placeholder text."""
    container = tk.Frame(parent, bg=BG_INPUT, bd=0,
                         highlightbackground=BORDER,
                         highlightthickness=1)
    container.pack(fill=X, pady=(4, 10))

    entry = tk.Entry(container, textvariable=var, font=FONT_INPUT,
                     bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=ACCENT2,
                     relief="flat", show=show, bd=8)
    entry.pack(fill=X)

    def on_focus_in(e):
        container.config(highlightbackground=ACCENT, highlightthickness=2)

    def on_focus_out(e):
        container.config(highlightbackground=BORDER, highlightthickness=1)

    entry.bind("<FocusIn>",  on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    entry.bind("<Return>",   lambda e: login_action())
    return entry


def _separator(parent):
    tk.Frame(parent, height=1, bg=BORDER).pack(fill=X, pady=8)


# ── Business logic ────────────────────────────────────────────────────────

def login_action():
    username = username_var.get().strip()
    password = password_var.get().strip()

    if not username:
        _show_error("Username is required!")
        return
    if not password:
        _show_error("Password is required!")
        return

    ok, role, data = backend.login(username, password)
    if not ok:
        _show_error(data)
        return

    app.destroy()
    if role == "doctor":
        subprocess.Popen([sys.executable,
                          os.path.join(BASE_DIR, "doctor_dashboard.py"),
                          username])
    else:
        subprocess.Popen([sys.executable,
                          os.path.join(BASE_DIR, "patient_dashboard.py"),
                          username, "", username, "", "", "", "", ""])


def signup_action():
    app.destroy()
    subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "signup.py")])


def _show_error(msg: str):
    status_var.set(msg)
    status_lbl.config(fg=DANGER)


def _clear_error(*_):
    status_var.set("")


# ── Build Window ──────────────────────────────────────────────────────────
app = ttk.Window(themename="darkly")
app.title("Hopify — Login")
app.geometry("460x660")
app.minsize(420, 520)
app.resizable(True, True)
app.configure(bg=BG_DARK)

# ── Scrollable canvas wrapper ─────────────────────────────────────────────
_canvas_wrap = tk.Frame(app, bg=BG_DARK)
_canvas_wrap.pack(fill=BOTH, expand=True)

_canvas = tk.Canvas(_canvas_wrap, bg=BG_DARK, bd=0, highlightthickness=0)
_scrollbar = tk.Scrollbar(_canvas_wrap, orient=VERTICAL, command=_canvas.yview)
_canvas.configure(yscrollcommand=_scrollbar.set)
_scrollbar.pack(side=RIGHT, fill=Y)
_canvas.pack(side=LEFT, fill=BOTH, expand=True)

outer = tk.Frame(_canvas, bg=BG_DARK)
_canvas_id = _canvas.create_window((0, 0), window=outer, anchor=NW)

def _on_frame_configure(e):
    _canvas.configure(scrollregion=_canvas.bbox("all"))

def _on_canvas_configure(e):
    _canvas.itemconfig(_canvas_id, width=e.width)

outer.bind("<Configure>", _on_frame_configure)
_canvas.bind("<Configure>", _on_canvas_configure)
_canvas.bind_all("<MouseWheel>",
    lambda e: _canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

# Apply padding inside the outer frame
outer.config(padx=30, pady=20)

# ── Logo / branding ───────────────────────────────────────────────────────
logo_frame = tk.Frame(outer, bg=BG_DARK)
logo_frame.pack(fill=X, pady=(0, 14))

tk.Label(logo_frame, text="HOPIFY", font=FONT_LOGO,
         bg=BG_DARK, fg=TEXT_MAIN).pack()
tk.Label(logo_frame, text="Your Health, Our Priority",
         font=FONT_SMALL, bg=BG_DARK, fg=TEXT_HINT).pack()

# ── Card ──────────────────────────────────────────────────────────────────
card = tk.Frame(outer, bg=BG_CARD, bd=0,
                highlightbackground=BORDER, highlightthickness=1)
card.pack(fill=X, padx=0, pady=0)

inner = tk.Frame(card, bg=BG_CARD, padx=24, pady=24)
inner.pack(fill=BOTH)

tk.Label(inner, text="Welcome Back", font=FONT_H1,
         bg=BG_CARD, fg=TEXT_MAIN).pack(anchor=W)
tk.Label(inner, text="Sign in to your Hopify account",
         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_SUB).pack(anchor=W, pady=(2, 16))

# Username
tk.Label(inner, text="USERNAME", font=FONT_LABEL,
         bg=BG_CARD, fg=TEXT_SUB).pack(anchor=W)
username_var = tk.StringVar()
username_var.trace_add("write", _clear_error)
_make_entry(inner, username_var)

# Password
tk.Label(inner, text="PASSWORD", font=FONT_LABEL,
         bg=BG_CARD, fg=TEXT_SUB).pack(anchor=W)
password_var = tk.StringVar()
password_var.trace_add("write", _clear_error)
_make_entry(inner, password_var, show="*")

# Status label
status_var = tk.StringVar()
status_lbl = tk.Label(inner, textvariable=status_var,
                       font=FONT_SMALL, bg=BG_CARD, fg=DANGER,
                       wraplength=340, justify=LEFT)
status_lbl.pack(anchor=W, pady=(0, 10))

# Login button
login_btn = tk.Button(inner, text="LOGIN", font=FONT_BTN,
                       bg=ACCENT, fg="#ffffff", activebackground=ACCENT2,
                       activeforeground="#ffffff", relief="flat",
                       cursor="hand2", bd=0, padx=10, pady=11,
                       command=login_action)
login_btn.pack(fill=X, pady=(0, 10))

def _on_login_enter(e):  login_btn.config(bg=ACCENT2)
def _on_login_leave(e):  login_btn.config(bg=ACCENT)
login_btn.bind("<Enter>", _on_login_enter)
login_btn.bind("<Leave>", _on_login_leave)

_separator(inner)

# Signup link
bottom = tk.Frame(inner, bg=BG_CARD)
bottom.pack(fill=X)
tk.Label(bottom, text="Don't have an account? ",
         font=FONT_SMALL, bg=BG_CARD, fg=TEXT_SUB).pack(side=LEFT)
sign_lbl = tk.Label(bottom, text="Sign Up",
                     font=(FONT_SMALL[0], FONT_SMALL[1], "underline"),
                     bg=BG_CARD, fg=ACCENT2, cursor="hand2")
sign_lbl.pack(side=LEFT)
sign_lbl.bind("<Button-1>", lambda e: signup_action())

app.mainloop()