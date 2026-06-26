"""
Hopify — Patient Dashboard
Refined dark-theme UI matching the login/signup aesthetic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import sys
import subprocess
import os

try:
    import ttkbootstrap as tbs
    USE_BOOTSTRAP = True
except ImportError:
    USE_BOOTSTRAP = False

# ── Palette (matches login/signup) ────────────────────────────────────────
BG_DARK     = "#0f1117"
BG_MAIN     = "#13151f"
BG_CARD     = "#1a1d2e"
BG_SIDEBAR  = "#12152a"
BG_INPUT    = "#252840"
ACCENT      = "#6c63ff"
ACCENT2     = "#a78bfa"
SUCCESS     = "#22d3a5"
WARNING     = "#f59e0b"
DANGER      = "#f87171"
TEXT_MAIN   = "#e2e8f0"
TEXT_SUB    = "#94a3b8"
TEXT_HINT   = "#64748b"
BORDER      = "#1e2540"
SB_ACTIVE   = "#252850"
SB_HOVER    = "#1c1f3a"
WHITE       = "#ffffff"

FONT_LOGO   = ("Segoe UI", 16, "bold")
FONT_H1     = ("Segoe UI", 15, "bold")
FONT_H2     = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_NAV    = ("Segoe UI", 10)
FONT_STAT   = ("Segoe UI", 24, "bold")
FONT_LABEL  = ("Segoe UI", 9, "bold")

if USE_BOOTSTRAP:
    BaseWindow   = tbs.Window
    _BASE_KWARGS = {"themename": "darkly"}
else:
    BaseWindow   = tk.Tk
    _BASE_KWARGS = {}

args     = sys.argv[1:]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class PatientDashboard(BaseWindow):

    def __init__(self):
        super().__init__(**_BASE_KWARGS)
        self.title("Hopify — Patient Dashboard")
        self.geometry("1250x780")
        self.minsize(1000, 650)
        self.configure(bg=BG_DARK)
        self._center_window()

        self.pages        = {}
        self._nav_buttons = {}

        self.patient = {
            "name":    args[0] if len(args) > 0 else "Patient",
            "phone":   args[1] if len(args) > 1 else "",
            "id":      args[2] if len(args) > 2 else "N/A",
            "age":     args[4] if len(args) > 4 else "",
            "blood":   args[5] if len(args) > 5 else "",
            "gender":  args[6] if len(args) > 6 else "",
            "address": args[7] if len(args) > 7 else "",
            "email":   "",
            "joined":  "2025",
        }

        self.active_nav = tk.StringVar(value="Dashboard")
        self._build_ui()
        self.set_active("Dashboard")

    # ── Helpers ───────────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = 1250, 780
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── Layout ────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = tk.Frame(self, bg=BG_DARK)
        root.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar(root).pack(side=tk.LEFT, fill=tk.Y)

        self.main = tk.Frame(root, bg=BG_MAIN)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_topbar(self.main)
        self.page_container = tk.Frame(self.main, bg=BG_MAIN)
        self.page_container.pack(fill=tk.BOTH, expand=True)

    # ── Sidebar ───────────────────────────────────────────────────────────

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG_SIDEBAR, width=220)
        sb.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(sb, bg=BG_SIDEBAR, pady=24)
        logo_frame.pack(fill=tk.X, padx=18)
        tk.Label(logo_frame, text="HOPIFY", bg=BG_SIDEBAR,
                 fg=WHITE, font=FONT_LOGO).pack(side=tk.LEFT)

        tk.Label(sb, text="Patient Portal", bg=BG_SIDEBAR,
                 fg=TEXT_HINT, font=FONT_SMALL).pack(anchor=tk.W, padx=22, pady=(0, 14))

        self._sidebar_divider(sb)

        nav_items = ["Dashboard", "Appointments", "Medical Records", "My Profile", "Settings"]
        for label in nav_items:
            self._nav_item(sb, label)

        tk.Frame(sb, bg=BG_SIDEBAR).pack(fill=tk.Y, expand=True)
        self._sidebar_divider(sb)

        # User card with initials avatar
        user_frame = tk.Frame(sb, bg=SB_HOVER, padx=14, pady=10)
        user_frame.pack(fill=tk.X, padx=10, pady=10)

        name_parts = self.patient["name"].split()
        display_name = (name_parts[0] + " " + name_parts[-1]
                        if len(name_parts) > 1 else
                        name_parts[0] if name_parts else "Patient")
        initials = "".join(p[0].upper() for p in name_parts if p)[:2]

        av = tk.Frame(user_frame, bg=ACCENT, width=36, height=36)
        av.pack(side=tk.LEFT, padx=(0, 10))
        av.pack_propagate(False)
        tk.Label(av, text=initials, bg=ACCENT, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        info = tk.Frame(user_frame, bg=SB_HOVER)
        info.pack(side=tk.LEFT)
        tk.Label(info, text=display_name, bg=SB_HOVER, fg=TEXT_MAIN,
                 font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        tk.Label(info, text=self.patient["id"], bg=SB_HOVER,
                 fg=TEXT_HINT, font=FONT_SMALL).pack(anchor=tk.W)

        self._nav_item(sb, "Logout", danger=True)
        return sb

    def _sidebar_divider(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, padx=14, pady=6)

    def _nav_item(self, parent, label, danger=False):
        fg_default = DANGER if danger else TEXT_SUB

        frame = tk.Frame(parent, bg=BG_SIDEBAR, cursor="hand2", padx=16, pady=9)
        frame.pack(fill=tk.X, padx=6, pady=1)

        text_lbl = tk.Label(frame, text=label, bg=BG_SIDEBAR,
                            fg=fg_default, font=FONT_NAV, anchor=tk.W)
        text_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        accent_bar = tk.Frame(frame, bg=ACCENT, width=3)
        self._nav_buttons[label] = (frame, text_lbl, accent_bar)

        for w in [frame, text_lbl]:
            w.bind("<Button-1>", lambda e, lbl=label: self.set_active(lbl))
            w.bind("<Enter>", lambda e, f=frame, t=text_lbl, lbl=label:
                   (f.config(bg=SB_HOVER), t.config(bg=SB_HOVER))
                   if lbl != self.active_nav.get() else None)
            w.bind("<Leave>", lambda e, f=frame, t=text_lbl, lbl=label:
                   (f.config(bg=BG_SIDEBAR), t.config(bg=BG_SIDEBAR))
                   if lbl != self.active_nav.get() else None)

    def set_active(self, lbl):
        if lbl not in self._nav_buttons:
            return

        if lbl == "Logout":
            if messagebox.askyesno("Hopify", "Are you sure you want to logout?"):
                self.destroy()
                subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "login_page.py")])
            return

        for btn_lbl, (f, t, a) in self._nav_buttons.items():
            is_danger = (btn_lbl == "Logout")
            f.config(bg=BG_SIDEBAR)
            t.config(bg=BG_SIDEBAR, fg=DANGER if is_danger else TEXT_SUB, font=FONT_NAV)
            a.pack_forget()

        f, t, a = self._nav_buttons[lbl]
        f.config(bg=SB_ACTIVE)
        t.config(bg=SB_ACTIVE, fg=WHITE, font=("Segoe UI", 10, "bold"))
        a.pack(side=tk.RIGHT, fill=tk.Y)

        self.active_nav.set(lbl)
        self._show_page(lbl)

    # ── Topbar ────────────────────────────────────────────────────────────

    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=BG_CARD, pady=14)
        bar.pack(fill=tk.X)
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X)

        left = tk.Frame(bar, bg=BG_CARD)
        left.pack(side=tk.LEFT, padx=24)
        self.topbar_title = tk.Label(left, text="Dashboard", bg=BG_CARD,
                                      fg=TEXT_MAIN, font=FONT_H1)
        self.topbar_title.pack(anchor=tk.W)
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        tk.Label(left, text=today, bg=BG_CARD, fg=TEXT_HINT,
                 font=FONT_SMALL).pack(anchor=tk.W)

        right = tk.Frame(bar, bg=BG_CARD)
        right.pack(side=tk.RIGHT, padx=24)
        btn = tk.Button(right, text="Book Appointment", bg=ACCENT, fg=WHITE,
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                        cursor="hand2", padx=14, pady=7,
                        activebackground=ACCENT2, activeforeground=WHITE,
                        bd=0, command=self._book_appointment_dialog)
        btn.pack(side=tk.LEFT)
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

    # ── Page routing ──────────────────────────────────────────────────────

    def _show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()

        if name not in self.pages:
            frame = tk.Frame(self.page_container, bg=BG_MAIN)
            if name == "Dashboard":
                self._build_dashboard_page(frame)
            elif name == "Appointments":
                self._build_appointments_page(frame)
            elif name == "Medical Records":
                self._build_medical_records_page(frame)
            elif name == "My Profile":
                self._build_profile_page(frame)
            else:
                self._build_placeholder_page(frame, name)
            self.pages[name] = frame

        self.pages[name].pack(fill=tk.BOTH, expand=True)

        titles = {
            "Dashboard":       "Dashboard",
            "Appointments":    "My Appointments",
            "Medical Records": "Medical Records",
            "My Profile":      "My Profile",
            "Settings":        "Settings",
        }
        if hasattr(self, "topbar_title"):
            self.topbar_title.config(text=titles.get(name, name))

    def _build_placeholder_page(self, parent, name):
        card = self._card(parent, fill=BOTH, expand=True)
        tk.Label(card, text=name, bg=BG_CARD, fg=TEXT_MAIN,
                 font=FONT_H1).pack(pady=(40, 8))
        tk.Label(card, text="This section is under development.",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_BODY).pack()

    # ── Scrollable helper ─────────────────────────────────────────────────

    def _scrollable(self, parent):
        canvas = tk.Canvas(parent, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(canvas, bg=BG_MAIN)
        win = canvas.create_window((0, 0), window=inner, anchor=tk.NW)

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",
            lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        return inner

    # ── Card / section helpers ────────────────────────────────────────────

    def _card(self, parent, **pack_kw):
        c = tk.Frame(parent, bg=BG_CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        c.pack(**pack_kw)
        return c

    def _section_header(self, parent, text, btn_text=None, btn_cmd=None):
        row = tk.Frame(parent, bg=BG_CARD, pady=14)
        row.pack(fill=tk.X, padx=20)
        tk.Label(row, text=text, bg=BG_CARD, fg=TEXT_MAIN,
                 font=FONT_H2).pack(side=tk.LEFT)
        if btn_text and btn_cmd:
            lbl = tk.Label(row, text=btn_text, bg=BG_CARD, fg=ACCENT2,
                           font=("Segoe UI", 9), cursor="hand2")
            lbl.pack(side=tk.RIGHT)
            lbl.bind("<Button-1>", lambda e: btn_cmd())
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, padx=20)

    def _styled_tree(self, parent, columns, headings, col_widths=None):
        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=BG_CARD, foreground=TEXT_MAIN,
                        fieldbackground=BG_CARD, rowheight=32,
                        borderwidth=0, font=FONT_BODY)
        style.configure("Dark.Treeview.Heading",
                        background=BG_INPUT, foreground=TEXT_SUB,
                        font=FONT_LABEL, borderwidth=0, relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", SB_ACTIVE)],
                  foreground=[("selected", WHITE)])

        tree = ttk.Treeview(parent, columns=columns,
                            show="headings", style="Dark.Treeview")
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
        if col_widths:
            for col, w in zip(columns, col_widths):
                tree.column(col, width=w, anchor=tk.CENTER if w < 180 else tk.W)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 16))
        return tree

    # ── Dashboard page ────────────────────────────────────────────────────

    def _build_dashboard_page(self, parent):
        inner = self._scrollable(parent)
        self._welcome_banner(inner)
        self._quick_stats(inner)
        self._dashboard_body(inner)

    def _welcome_banner(self, parent):
        banner = tk.Frame(parent, bg=ACCENT, height=100)
        banner.pack(fill=tk.X, padx=28, pady=(24, 0))
        banner.pack_propagate(False)

        left = tk.Frame(banner, bg=ACCENT)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=28, pady=18)

        hour = datetime.datetime.now().hour
        greeting = ("Good Morning" if hour < 12
                    else "Good Afternoon" if hour < 17
                    else "Good Evening")

        name_parts = self.patient["name"].split()
        first_name = name_parts[0] if name_parts else "Patient"

        tk.Label(left, text=f"{greeting}, {first_name}",
                 bg=ACCENT, fg=WHITE,
                 font=("Segoe UI", 15, "bold")).pack(anchor=tk.W)
        tk.Label(left,
                 text=f"Patient ID: {self.patient['id']}  •  Welcome to your Hopify portal.",
                 bg=ACCENT, fg="#d4cfff",
                 font=FONT_BODY).pack(anchor=tk.W, pady=(4, 0))

    def _quick_stats(self, parent):
        tk.Label(parent, text="OVERVIEW", bg=BG_MAIN, fg=TEXT_HINT,
                 font=FONT_LABEL).pack(anchor=tk.W, padx=28, pady=(20, 8))

        row = tk.Frame(parent, bg=BG_MAIN)
        row.pack(fill=tk.X, padx=28, pady=(0, 20))

        stats = [
            ("Upcoming Appointments", "—", "No upcoming",     ACCENT),
            ("Medical Records",       "—", "None yet",        SUCCESS),
            ("Active Prescriptions",  "—", "None prescribed", WARNING),
            ("Last Visit",            "—", "Not recorded",    DANGER),
        ]
        for i, (title, val, sub, color) in enumerate(stats):
            card = tk.Frame(row, bg=BG_CARD, padx=16, pady=14,
                            highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=0, column=i, sticky=tk.NSEW, padx=(0, 14) if i < 3 else 0)
            row.columnconfigure(i, weight=1)

            bar = tk.Frame(card, bg=color, width=4)
            bar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14))

            body = tk.Frame(card, bg=BG_CARD)
            body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tk.Label(body, text=title, bg=BG_CARD, fg=TEXT_HINT,
                     font=FONT_SMALL, wraplength=120, justify=tk.LEFT).pack(anchor=tk.W)
            tk.Label(body, text=val, bg=BG_CARD, fg=TEXT_MAIN,
                     font=FONT_STAT).pack(anchor=tk.W, pady=(6, 2))
            tk.Label(body, text=sub, bg=BG_CARD, fg=color,
                     font=FONT_SMALL).pack(anchor=tk.W)

    def _dashboard_body(self, parent):
        cols = tk.Frame(parent, bg=BG_MAIN)
        cols.pack(fill=tk.X, padx=28, pady=(0, 24))
        cols.columnconfigure(0, weight=3)
        cols.columnconfigure(1, weight=2)

        self._upcoming_appointments_card(cols)
        self._right_panel(cols)

    def _upcoming_appointments_card(self, parent):
        card = tk.Frame(parent, bg=BG_CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        card.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 14))

        self._section_header(card, "Upcoming Appointments",
                              btn_text="View All",
                              btn_cmd=lambda: self._activate_nav("Appointments"))

        empty = tk.Frame(card, bg=BG_CARD, pady=36)
        empty.pack(fill=tk.X)
        tk.Label(empty, text="No upcoming appointments",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_BODY).pack()
        tk.Label(empty, text="Book one to get started.",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_SMALL).pack(pady=(4, 12))

        btn = tk.Button(empty, text="Book Appointment", bg=ACCENT, fg=WHITE,
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                        cursor="hand2", padx=14, pady=7,
                        activebackground=ACCENT2, activeforeground=WHITE,
                        command=self._book_appointment_dialog)
        btn.pack()
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

        tk.Frame(card, bg=BG_CARD, height=14).pack()

    def _right_panel(self, parent):
        right = tk.Frame(parent, bg=BG_MAIN)
        right.grid(row=0, column=1, sticky=tk.NSEW)

        # Profile card
        pcard = tk.Frame(right, bg=BG_CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        pcard.pack(fill=tk.X, pady=(0, 14))

        self._section_header(pcard, "My Profile")

        body = tk.Frame(pcard, bg=BG_CARD, padx=18, pady=10)
        body.pack(fill=tk.X)

        for key, val in [
            ("Name",  self.patient["name"]),
            ("ID",    self.patient["id"]),
            ("Age",   (str(self.patient["age"]) + " yrs") if self.patient["age"] else "—"),
            ("Blood", self.patient["blood"] or "—"),
            ("Phone", self.patient["phone"] or "—"),
        ]:
            row = tk.Frame(body, bg=BG_CARD)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=key + ":", bg=BG_CARD, fg=TEXT_HINT,
                     font=FONT_SMALL, width=7, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=val, bg=BG_CARD, fg=TEXT_MAIN,
                     font=("Segoe UI", 9, "bold"), anchor=tk.W).pack(side=tk.LEFT)

        lbl = tk.Label(pcard, text="Edit Profile", bg=BG_CARD, fg=ACCENT2,
                       font=("Segoe UI", 9), cursor="hand2")
        lbl.pack(anchor=tk.W, padx=18, pady=(6, 14))
        lbl.bind("<Button-1>", lambda e: self._activate_nav("My Profile"))

        # Quick actions
        qa_card = tk.Frame(right, bg=BG_CARD,
                           highlightbackground=BORDER, highlightthickness=1)
        qa_card.pack(fill=tk.X)

        self._section_header(qa_card, "Quick Actions")

        actions = [
            ("Book Appointment", ACCENT,   self._book_appointment_dialog),
            ("View Records",     SUCCESS,  lambda: self._activate_nav("Medical Records")),
            ("Update Profile",   ACCENT2,  lambda: self._activate_nav("My Profile")),
        ]
        qa_body = tk.Frame(qa_card, bg=BG_CARD, padx=14, pady=10)
        qa_body.pack(fill=tk.X)
        for label, color, cmd in actions:
            btn = tk.Button(qa_body, text=label, bg=BG_INPUT, fg=TEXT_MAIN,
                            font=FONT_BODY, relief=tk.FLAT, cursor="hand2",
                            padx=12, pady=8, activebackground=color,
                            activeforeground=WHITE, anchor=tk.W, bd=0,
                            command=cmd)
            btn.pack(fill=tk.X, pady=3)
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=c, fg=WHITE))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_INPUT, fg=TEXT_MAIN))

        tk.Frame(qa_card, bg=BG_CARD, height=8).pack()

    # ── Appointments page ─────────────────────────────────────────────────

    def _build_appointments_page(self, parent):
        inner = self._scrollable(parent)

        hdr = tk.Frame(inner, bg=BG_MAIN)
        hdr.pack(fill=tk.X, padx=28, pady=(24, 14))
        tk.Label(hdr, text="My Appointments", bg=BG_MAIN,
                 fg=TEXT_MAIN, font=FONT_H1).pack(side=tk.LEFT)
        btn = tk.Button(hdr, text="Book New", bg=ACCENT, fg=WHITE,
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                        cursor="hand2", padx=14, pady=7,
                        activebackground=ACCENT2, activeforeground=WHITE,
                        command=self._book_appointment_dialog)
        btn.pack(side=tk.RIGHT)
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

        card = self._card(inner, fill=tk.X, padx=28, pady=(0, 24))

        col_frame = tk.Frame(card, bg=BG_INPUT, pady=8)
        col_frame.pack(fill=tk.X, padx=0)
        for h, w in zip(["Doctor", "Department", "Date", "Time", "Status"],
                        [20, 16, 14, 12, 12]):
            tk.Label(col_frame, text=h, width=w, bg=BG_INPUT,
                     fg=TEXT_HINT, font=FONT_LABEL, anchor=tk.W).pack(
                         side=tk.LEFT, padx=14)

        empty = tk.Frame(card, bg=BG_CARD, pady=40)
        empty.pack(fill=tk.X)
        tk.Label(empty, text="No appointments found",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_BODY).pack(pady=(0, 4))
        tk.Label(empty, text="Your booked appointments will appear here.",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_SMALL).pack()
        btn2 = tk.Button(empty, text="Book Appointment", bg=ACCENT, fg=WHITE,
                         font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                         cursor="hand2", padx=14, pady=7,
                         activebackground=ACCENT2, activeforeground=WHITE,
                         command=self._book_appointment_dialog)
        btn2.pack(pady=(14, 0))
        btn2.bind("<Enter>", lambda e: btn2.config(bg=ACCENT2))
        btn2.bind("<Leave>", lambda e: btn2.config(bg=ACCENT))
        tk.Frame(card, bg=BG_CARD, height=16).pack()

    # ── Medical records page ──────────────────────────────────────────────

    def _build_medical_records_page(self, parent):
        inner = self._scrollable(parent)

        hdr = tk.Frame(inner, bg=BG_MAIN)
        hdr.pack(fill=tk.X, padx=28, pady=(24, 14))
        tk.Label(hdr, text="Medical Records", bg=BG_MAIN,
                 fg=TEXT_MAIN, font=FONT_H1).pack(side=tk.LEFT)

        sections = [
            ("Diagnoses",     "No diagnoses recorded yet."),
            ("Prescriptions", "No active prescriptions."),
            ("Lab Reports",   "No lab reports uploaded."),
            ("Documents",     "No documents attached."),
        ]
        for title, empty_msg in sections:
            card = self._card(inner, fill=tk.X, padx=28, pady=(0, 14))
            self._section_header(card, title)
            empty = tk.Frame(card, bg=BG_CARD, pady=20)
            empty.pack(fill=tk.X)
            tk.Label(empty, text=empty_msg, bg=BG_CARD,
                     fg=TEXT_HINT, font=FONT_BODY).pack()
            tk.Frame(card, bg=BG_CARD, height=10).pack()

    # ── Profile page ──────────────────────────────────────────────────────

    def _build_profile_page(self, parent):
        inner = self._scrollable(parent)

        tk.Label(inner, text="My Profile", bg=BG_MAIN,
                 fg=TEXT_MAIN, font=FONT_H1).pack(
                     anchor=tk.W, padx=28, pady=(24, 14))

        cols = tk.Frame(inner, bg=BG_MAIN)
        cols.pack(fill=tk.X, padx=28, pady=(0, 24))
        cols.columnconfigure(0, weight=2)
        cols.columnconfigure(1, weight=3)

        # Left: summary card
        left = tk.Frame(cols, bg=BG_CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        left.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 14))

        name_parts = self.patient["name"].split()
        initials = "".join(p[0].upper() for p in name_parts if p)[:2]

        avatar_wrap = tk.Frame(left, bg=BG_CARD, pady=24)
        avatar_wrap.pack()
        av = tk.Frame(avatar_wrap, bg=ACCENT, width=80, height=80)
        av.pack()
        av.pack_propagate(False)
        tk.Label(av, text=initials, bg=ACCENT, fg=WHITE,
                 font=("Segoe UI", 28, "bold")).place(relx=0.5, rely=0.5,
                                                       anchor=tk.CENTER)

        tk.Label(left, text=self.patient["name"], bg=BG_CARD,
                 fg=TEXT_MAIN, font=("Segoe UI", 12, "bold")).pack()
        tk.Label(left, text=self.patient["id"], bg=BG_CARD,
                 fg=TEXT_HINT, font=FONT_SMALL).pack(pady=(2, 0))
        tk.Label(left, text=f"Member since {self.patient['joined']}",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_SMALL).pack(pady=(2, 0))

        tk.Frame(left, bg=BORDER, height=1).pack(fill=tk.X, padx=18, pady=14)

        for lbl_text, val in [
            ("Blood Type", self.patient["blood"] or "—"),
            ("Age",        (str(self.patient["age"]) + " years") if self.patient["age"] else "—"),
            ("Gender",     self.patient["gender"] or "—"),
        ]:
            row = tk.Frame(left, bg=BG_CARD)
            row.pack(fill=tk.X, padx=18, pady=3)
            tk.Label(row, text=lbl_text + ":", bg=BG_CARD, fg=TEXT_HINT,
                     font=FONT_SMALL, width=12, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=val, bg=BG_CARD, fg=TEXT_MAIN,
                     font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        tk.Frame(left, bg=BG_CARD, height=18).pack()

        # Right: editable fields
        right = tk.Frame(cols, bg=BG_CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        right.grid(row=0, column=1, sticky=tk.NSEW)

        self._section_header(right, "Personal Information")

        fields = [
            ("Full Name",         self.patient["name"]),
            ("Phone Number",      self.patient["phone"]),
            ("Email Address",     self.patient["email"]),
            ("Address",           self.patient["address"]),
            ("Date of Birth",     ""),
            ("Emergency Contact", ""),
        ]
        form = tk.Frame(right, bg=BG_CARD, padx=20, pady=12)
        form.pack(fill=tk.X)

        for field_label, default in fields:
            tk.Label(form, text=field_label, bg=BG_CARD, fg=TEXT_SUB,
                     font=FONT_LABEL, anchor=tk.W).pack(anchor=tk.W, pady=(8, 2))
            ef = tk.Frame(form, bg=BG_INPUT,
                          highlightbackground=BORDER, highlightthickness=1)
            ef.pack(fill=tk.X)
            e = tk.Entry(ef, font=FONT_BODY, bd=0, bg=BG_INPUT,
                         fg=TEXT_MAIN, insertbackground=ACCENT2)
            e.insert(0, default)
            e.pack(fill=tk.X, padx=10, pady=7)
            e.bind("<FocusIn>",  lambda ev, f=ef: f.config(highlightbackground=ACCENT))
            e.bind("<FocusOut>", lambda ev, f=ef: f.config(highlightbackground=BORDER))

        btn = tk.Button(form, text="Save Changes", bg=ACCENT, fg=WHITE,
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                        cursor="hand2", padx=16, pady=8,
                        activebackground=ACCENT2, activeforeground=WHITE,
                        command=lambda: messagebox.showinfo(
                            "Hopify", "Profile updated successfully!"))
        btn.pack(anchor=tk.E, pady=(14, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT2))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))
        tk.Frame(right, bg=BG_CARD, height=16).pack()

    # ── Book appointment dialog ────────────────────────────────────────────

    def _book_appointment_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Book Appointment — Hopify")
        dialog.geometry("480x540")
        dialog.resizable(False, False)
        dialog.configure(bg=BG_CARD)
        dialog.grab_set()

        x = self.winfo_x() + (self.winfo_width()  - 480) // 2
        y = self.winfo_y() + (self.winfo_height() - 540) // 2
        dialog.geometry(f"480x540+{x}+{y}")

        # Header
        hdr = tk.Frame(dialog, bg=ACCENT, pady=18)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="Book New Appointment", bg=ACCENT, fg=WHITE,
                 font=("Segoe UI", 13, "bold")).pack(padx=20, anchor=tk.W)
        tk.Label(hdr, text=f"Patient: {self.patient['name']}  ({self.patient['id']})",
                 bg=ACCENT, fg="#d4cfff", font=FONT_SMALL).pack(padx=20, anchor=tk.W)

        form = tk.Frame(dialog, bg=BG_CARD, padx=24, pady=16)
        form.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("Doctor / Specialist", "e.g. Dr. Sharma"),
            ("Department",          "e.g. Cardiology"),
            ("Preferred Date",      "YYYY-MM-DD"),
            ("Preferred Time",      "e.g. 10:00 AM"),
            ("Reason / Notes",      "Brief description"),
        ]

        entries = []
        for field_label, placeholder in fields:
            tk.Label(form, text=field_label, bg=BG_CARD, fg=TEXT_SUB,
                     font=FONT_LABEL, anchor=tk.W).pack(anchor=tk.W, pady=(8, 2))
            ef = tk.Frame(form, bg=BG_INPUT,
                          highlightbackground=BORDER, highlightthickness=1)
            ef.pack(fill=tk.X)
            e = tk.Entry(ef, font=FONT_BODY, bd=0, bg=BG_INPUT,
                         fg=TEXT_HINT, insertbackground=ACCENT2)
            e.insert(0, placeholder)
            e.pack(fill=tk.X, padx=10, pady=7)

            def on_in(event, ent=e, ph=placeholder, f=ef):
                if ent.get() == ph:
                    ent.delete(0, tk.END)
                    ent.config(fg=TEXT_MAIN)
                f.config(highlightbackground=ACCENT)

            def on_out(event, ent=e, ph=placeholder, f=ef):
                if ent.get().strip() == "":
                    ent.insert(0, ph)
                    ent.config(fg=TEXT_HINT)
                f.config(highlightbackground=BORDER)

            e.bind("<FocusIn>",  on_in)
            e.bind("<FocusOut>", on_out)
            entries.append((field_label, e, placeholder))

        def submit():
            messagebox.showinfo("Hopify",
                "Appointment request submitted!\n\nYou will be notified once confirmed.",
                parent=dialog)
            dialog.destroy()

        btn_row = tk.Frame(form, bg=BG_CARD)
        btn_row.pack(fill=tk.X, pady=(16, 0))

        cancel_btn = tk.Button(btn_row, text="Cancel", bg=BG_INPUT, fg=TEXT_SUB,
                               font=FONT_BODY, relief=tk.FLAT, padx=14, pady=8,
                               cursor="hand2", command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT)

        submit_btn = tk.Button(btn_row, text="Submit Request", bg=ACCENT, fg=WHITE,
                               font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                               padx=16, pady=8, cursor="hand2",
                               activebackground=ACCENT2, activeforeground=WHITE,
                               command=submit)
        submit_btn.pack(side=tk.RIGHT)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=ACCENT2))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=ACCENT))

    def _activate_nav(self, label):
        self.set_active(label)


if __name__ == "__main__":
    if not USE_BOOTSTRAP:
        print("ttkbootstrap not found — running with plain tkinter.")
    app = PatientDashboard()
    app.mainloop()