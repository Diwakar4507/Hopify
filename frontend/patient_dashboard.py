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

CLR_SIDEBAR    =   "#2C57BC"
CLR_SIDEBAR_LT = "#132D57"
CLR_PRIMARY    = "#1A73E8"
CLR_ACCENT     = "#00C9A7"
CLR_BG         = "#F4F7FE"
CLR_WHITE      = "#FFFFFF"
CLR_TEXT       = "#1E2A3A"
CLR_MUTED      = "#465C89"
CLR_BORDER     = "#E2E8F0"
CLR_DANGER     = "#EF4444"
CLR_WARNING    = "#F59E0B"
CLR_SUCCESS    = "#10B981"

FONT_LOGO  = ("Segoe UI", 18, "bold")
FONT_H1    = ("Segoe UI", 16, "bold")
FONT_H2    = ("Segoe UI", 13, "bold")
FONT_BODY  = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_NAV   = ("Segoe UI", 11)
FONT_STAT  = ("Segoe UI", 26, "bold")

if USE_BOOTSTRAP:
    BaseWindow = tbs.Window
    _BASE_KWARGS = {"themename": "litera"}
else:
    BaseWindow = tk.Tk
    _BASE_KWARGS = {}

args = sys.argv[1:]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PatientDashboard(BaseWindow):

    def __init__(self):
        super().__init__(**_BASE_KWARGS)
        self.title("HOPIFY — Patient Dashboard")
        self.geometry("1250x780")
        self.minsize(1000, 650)
        self.configure(bg=CLR_BG)
        self._center_window()

        self.pages = {}
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

    def _center_window(self):
        self.update_idletasks()
        w, h = 1250, 780
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        root = tk.Frame(self, bg=CLR_BG)
        root.pack(fill=tk.BOTH, expand=True)

        self.sidebar = self._build_sidebar(root)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main = tk.Frame(root, bg=CLR_BG)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_topbar(self.main)
        self.page_container = tk.Frame(self.main, bg=CLR_BG)
        self.page_container.pack(fill=tk.BOTH, expand=True)

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=CLR_SIDEBAR, width=220)
        sb.pack_propagate(False)

        logo_frame = tk.Frame(sb, bg=CLR_SIDEBAR, pady=22)
        logo_frame.pack(fill=tk.X, padx=18)
        tk.Label(logo_frame, text="🏥", bg=CLR_SIDEBAR, font=("Segoe UI Emoji", 22)).pack(side=tk.LEFT)
        tk.Label(logo_frame, text=" HOPIFY", bg=CLR_SIDEBAR, fg=CLR_WHITE, font=FONT_LOGO).pack(side=tk.LEFT)

        tk.Label(sb, text="Patient Portal", bg=CLR_SIDEBAR, fg="#F6F7F9", font=FONT_SMALL).pack(anchor=tk.W, padx=22, pady=(0, 14))

        self._sidebar_divider(sb)

        nav_items = [
            ("📊", "Dashboard"),
            ("📅", "Appointments"),
            ("📋", "Medical Records"),
            ("👤", "My Profile"),
            ("⚙️", "Settings"),
        ]
        for icon, label in nav_items:
            self._nav_item(sb, icon, label)

        tk.Frame(sb, bg=CLR_SIDEBAR).pack(fill=tk.Y, expand=True)
        self._sidebar_divider(sb)

        user_frame = tk.Frame(sb, bg=CLR_SIDEBAR_LT, padx=14, pady=10)
        user_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(user_frame, text="👤", bg=CLR_SIDEBAR_LT, font=("Segoe UI Emoji", 18)).pack(side=tk.LEFT, padx=(0, 8))
        info = tk.Frame(user_frame, bg=CLR_SIDEBAR_LT)
        info.pack(side=tk.LEFT)

        name_parts = self.patient["name"].split()
        display_name = name_parts[0] + " " + name_parts[-1] if len(name_parts) > 1 else (name_parts[0] if name_parts else "Patient")

        tk.Label(info, text=display_name, bg=CLR_SIDEBAR_LT, fg=CLR_WHITE, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        tk.Label(info, text=self.patient["id"], bg=CLR_SIDEBAR_LT, fg="#7A94BE", font=FONT_SMALL).pack(anchor=tk.W)

        self._nav_item(sb, "🚪", "Logout")
        return sb

    def _sidebar_divider(self, parent):
        tk.Frame(parent, bg="#1E3460", height=1).pack(fill=tk.X, padx=14, pady=6)

    def _nav_item(self, parent, icon, label):
        is_logout = (label == "Logout")
        frame = tk.Frame(parent, bg=CLR_SIDEBAR, cursor="hand2", padx=14, pady=8)
        frame.pack(fill=tk.X, padx=8, pady=1)

        icon_lbl = tk.Label(frame, text=icon, bg=CLR_SIDEBAR, fg=CLR_WHITE, font=("Segoe UI Emoji", 13))
        icon_lbl.pack(side=tk.LEFT, padx=(0, 10))

        text_lbl = tk.Label(frame, text=label, bg=CLR_SIDEBAR, fg="#A8C0E0" if not is_logout else "#EF8080", font=FONT_NAV, anchor=tk.W)
        text_lbl.pack(side=tk.LEFT, fill=tk.X)

        accent = tk.Frame(frame, bg=CLR_ACCENT, width=4)

        self._nav_buttons[label] = (frame, text_lbl, icon_lbl, accent)

        def on_enter(e, f=frame, t=text_lbl, i=icon_lbl, lbl=label):
            if lbl != self.active_nav.get():
                f.config(bg="#162848")
                t.config(bg="#162848")
                i.config(bg="#162848")

        def on_leave(e, f=frame, t=text_lbl, i=icon_lbl, lbl=label):
            if lbl != self.active_nav.get():
                f.config(bg=CLR_SIDEBAR)
                t.config(bg=CLR_SIDEBAR)
                i.config(bg=CLR_SIDEBAR)

        for w in [frame, icon_lbl, text_lbl]:
            w.bind("<Button-1>", lambda e, target=label: self.set_active(target))
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

    def set_active(self, lbl):
        if lbl not in self._nav_buttons:
            return

        if lbl == "Logout":
            if messagebox.askyesno("HOPIFY", "Are you sure you want to logout?"):
                self.destroy()
                subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "login_page.py")])
            return

        for btn_lbl, (btn_f, btn_t, btn_i, btn_a) in self._nav_buttons.items():
            btn_f.config(bg=CLR_SIDEBAR)
            btn_t.config(bg=CLR_SIDEBAR, fg="#A8C0E0" if btn_lbl != "Logout" else "#EF8080", font=FONT_NAV)
            btn_i.config(bg=CLR_SIDEBAR)
            btn_a.pack_forget()

        f, t, i, a = self._nav_buttons[lbl]
        f.config(bg="#1B3867")
        t.config(bg="#1B3867", fg=CLR_WHITE, font=("Segoe UI", 11, "bold"))
        i.config(bg="#1B3867")
        a.pack(side=tk.LEFT, fill=tk.Y, padx=(4, 0))

        self.active_nav.set(lbl)
        self._show_page(lbl)

    def _activate_nav(self, label):
        self.set_active(label)

    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=CLR_WHITE, pady=12)
        bar.pack(fill=tk.X)
        tk.Frame(parent, bg=CLR_BORDER, height=1).pack(fill=tk.X)

        left = tk.Frame(bar, bg=CLR_WHITE)
        left.pack(side=tk.LEFT, padx=24)
        self.topbar_title = tk.Label(left, text="Patient Dashboard", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H1)
        self.topbar_title.pack(anchor=tk.W)
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        tk.Label(left, text=today, bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack(anchor=tk.W)

        right = tk.Frame(bar, bg=CLR_WHITE)
        right.pack(side=tk.RIGHT, padx=24)

        tk.Button(left, text="Book Appointment →", bg=CLR_ACCENT, fg=CLR_WHITE, font=("Segoe UI", 9, "bold"),
          relief=tk.FLAT, cursor="hand2", padx=10, pady=2,
          activebackground="#00a88e", activeforeground=CLR_WHITE,
          command=self._book_appointment_dialog).pack(anchor=tk.W, pady=(4, 0))

        tk.Label(right, text="🔔", bg=CLR_WHITE, font=("Segoe UI Emoji", 14), cursor="hand2").pack(side=tk.LEFT, padx=4)

    def _show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()

        if name not in self.pages:
            frame = tk.Frame(self.page_container, bg=CLR_BG)
            if name == "Dashboard":
                self._build_dashboard_page(frame)
            elif name == "Appointments":
                self._build_appointments_page(frame)
            elif name == "Medical Records":
                self._build_medical_records_page(frame)
            elif name == "My Profile":
                self._build_profile_page(frame)
            else:
                tk.Label(frame, text=f"  {name}  ", bg=CLR_BG, fg=CLR_MUTED, font=("Segoe UI", 14)).pack(expand=True)
            self.pages[name] = frame

        self.pages[name].pack(fill=tk.BOTH, expand=True)

        titles = {
            "Dashboard":       "Patient Dashboard",
            "Appointments":    "My Appointments",
            "Medical Records": "Medical Records",
            "My Profile":      "My Profile",
            "Settings":        "Settings",
        }
        if hasattr(self, "topbar_title"):
            self.topbar_title.config(text=titles.get(name, name))

    def _scrollable(self, parent):
        canvas = tk.Canvas(parent, bg=CLR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(canvas, bg=CLR_BG)
        win = canvas.create_window((0, 0), window=inner, anchor=tk.NW)

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        return inner

    def _build_dashboard_page(self, parent):
        inner = self._scrollable(parent)
        self._welcome_banner(inner)
        self._quick_stats(inner)
        self._dashboard_body(inner)

    def _welcome_banner(self, parent):
        banner = tk.Frame(parent, bg=CLR_PRIMARY, height=110)
        banner.pack(fill=tk.X, padx=28, pady=(24, 0))
        banner.pack_propagate(False)

        left = tk.Frame(banner, bg=CLR_PRIMARY)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=28, pady=16)

        hour = datetime.datetime.now().hour
        greeting = ("Good Morning" if hour < 12 else "Good Afternoon" if hour < 17 else "Good Evening")

        tk.Label(left, text=f"{greeting}, {self.patient['name']} 👋", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 15, "bold")).pack(anchor=tk.W)
        tk.Label(left, text=f"Patient ID: {self.patient['id']}  •  Welcome to your HOPIFY portal.", bg=CLR_PRIMARY, fg="#B8D4FF", font=FONT_BODY).pack(anchor=tk.W, pady=(4, 10))

        right = tk.Frame(banner, bg=CLR_PRIMARY)
        right.pack(side=tk.RIGHT, padx=28)
        tk.Label(right, text="🏥", bg=CLR_PRIMARY, font=("Segoe UI Emoji", 48)).pack()
    def _quick_stats(self, parent):
        tk.Label(parent, text="Quick Overview", bg=CLR_BG, fg=CLR_MUTED, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=28, pady=(22, 8))

        row = tk.Frame(parent, bg=CLR_BG)
        row.pack(fill=tk.X, padx=28, pady=(0, 22))

        stats = [
            ("📅", "Upcoming Appointments", "—", "No upcoming",     CLR_PRIMARY),
            ("📋", "Medical Records",        "—", "None yet",        CLR_SUCCESS),
            ("💊", "Active Prescriptions",   "—", "None prescribed", CLR_ACCENT),
            ("📆", "Last Visit",             "—", "Not recorded",    CLR_WARNING),
        ]
        for i, (icon, title, val, sub, color) in enumerate(stats):
            self._stat_card(row, icon, title, val, sub, color, i)

    def _stat_card(self, parent, icon, title, value, sub, color, col):
        card = tk.Frame(parent, bg=CLR_WHITE, padx=16, pady=14, highlightbackground=CLR_BORDER, highlightthickness=1)
        card.grid(row=0, column=col, sticky=tk.NSEW, padx=(0, 14) if col < 3 else 0)
        parent.columnconfigure(col, weight=1)

        top = tk.Frame(card, bg=CLR_WHITE)
        top.pack(fill=tk.X)

        icon_bg = tk.Frame(top, bg=color, width=42, height=42)
        icon_bg.pack(side=tk.LEFT)
        icon_bg.pack_propagate(False)
        tk.Label(icon_bg, text=icon, bg=color, font=("Segoe UI Emoji", 16)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(top, text=title, bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL, wraplength=110, justify=tk.LEFT).pack(side=tk.LEFT, padx=10, anchor=tk.W)
        tk.Label(card, text=value, bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_STAT).pack(anchor=tk.W, pady=(10, 2))
        tk.Label(card, text=sub, bg=CLR_WHITE, fg=color, font=FONT_SMALL).pack(anchor=tk.W)

        card.bind("<Enter>", lambda e, c=card: c.config(highlightbackground=color))
        card.bind("<Leave>", lambda e, c=card: c.config(highlightbackground=CLR_BORDER))

    def _dashboard_body(self, parent):
        cols = tk.Frame(parent, bg=CLR_BG)
        cols.pack(fill=tk.X, padx=28, pady=(0, 24))
        cols.columnconfigure(0, weight=3)
        cols.columnconfigure(1, weight=2)

        self._upcoming_appointments_card(cols)
        self._dashboard_right_panel(cols)

    def _upcoming_appointments_card(self, parent):
        card = tk.Frame(parent, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
        card.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 14))

        hdr = tk.Frame(card, bg=CLR_WHITE, pady=14)
        hdr.pack(fill=tk.X, padx=18)
        tk.Label(hdr, text="📅  Upcoming Appointments", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(side=tk.LEFT)
        tk.Button(hdr, text="View All →", bg=CLR_WHITE, fg=CLR_PRIMARY, font=("Segoe UI", 9), relief=tk.FLAT,
                  cursor="hand2", bd=0, command=lambda: self._activate_nav("Appointments")).pack(side=tk.RIGHT)

        empty = tk.Frame(card, bg=CLR_WHITE, pady=36)
        empty.pack(fill=tk.X)
        tk.Label(empty, text="📭", bg=CLR_WHITE, font=("Segoe UI Emoji", 32)).pack()
        tk.Label(empty, text="No upcoming appointments", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_BODY).pack(pady=(6, 2))
        tk.Label(empty, text="Book one to get started.", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack()
        tk.Button(empty, text="＋  Book Appointment", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", padx=14, pady=7,
                  activebackground="#1558b0", activeforeground=CLR_WHITE,
                  command=self._book_appointment_dialog).pack(pady=(12, 0))

        tk.Frame(card, bg=CLR_WHITE, height=14).pack()

    def _dashboard_right_panel(self, parent):
        right = tk.Frame(parent, bg=CLR_BG)
        right.grid(row=0, column=1, sticky=tk.NSEW)

        pcard = tk.Frame(right, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
        pcard.pack(fill=tk.X, pady=(0, 14))

        tk.Label(pcard, text="👤  My Profile", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(anchor=tk.W, padx=18, pady=(14, 8))

        avatar_frame = tk.Frame(pcard, bg=CLR_PRIMARY, width=64, height=64)
        avatar_frame.pack(padx=18, pady=(0, 8))
        avatar_frame.pack_propagate(False)
        tk.Label(avatar_frame, text="👤", bg=CLR_PRIMARY, font=("Segoe UI Emoji", 30)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for key, val in [
            ("Name",  self.patient["name"]),
            ("ID",    self.patient["id"]),
            ("Age",   str(self.patient["age"]) + " yrs"),
            ("Blood", self.patient["blood"]),
            ("Phone", self.patient["phone"]),
        ]:
            row = tk.Frame(pcard, bg=CLR_WHITE)
            row.pack(fill=tk.X, padx=18, pady=2)
            tk.Label(row, text=key + ":", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL, width=7, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=val, bg=CLR_WHITE, fg=CLR_TEXT, font=("Segoe UI", 9, "bold"), anchor=tk.W).pack(side=tk.LEFT)

        tk.Button(pcard, text="Edit Profile →", bg=CLR_BG, fg=CLR_PRIMARY, font=("Segoe UI", 9), relief=tk.FLAT,
                  cursor="hand2", command=lambda: self._activate_nav("My Profile")).pack(anchor=tk.W, padx=18, pady=(6, 14))

        qa_card = tk.Frame(right, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
        qa_card.pack(fill=tk.X)

        tk.Label(qa_card, text="⚡  Quick Actions", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(anchor=tk.W, padx=18, pady=(14, 10))

        actions = [
            ("📅", "Book Appointment", CLR_PRIMARY, self._book_appointment_dialog),
            ("📋", "View Records",     CLR_SUCCESS,  lambda: self._activate_nav("Medical Records")),
            ("👤", "Update Profile",   CLR_ACCENT,   lambda: self._activate_nav("My Profile")),
        ]
        for icon, label, color, cmd in actions:
            btn = tk.Frame(qa_card, bg=color, cursor="hand2", padx=12, pady=9)
            btn.pack(fill=tk.X, padx=14, pady=3)
            tk.Label(btn, text=icon, bg=color, font=("Segoe UI Emoji", 12)).pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(btn, text=label, bg=color, fg=CLR_WHITE, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
            tk.Label(btn, text="→", bg=color, fg=CLR_WHITE, font=FONT_BODY).pack(side=tk.RIGHT)
            for w in [btn] + list(btn.winfo_children()):
                w.bind("<Button-1>", lambda e, command_target=cmd: command_target())

        tk.Frame(qa_card, bg=CLR_WHITE, height=10).pack()

    def _build_appointments_page(self, parent):
        inner = self._scrollable(parent)

        hdr = tk.Frame(inner, bg=CLR_BG)
        hdr.pack(fill=tk.X, padx=28, pady=(24, 14))
        tk.Label(hdr, text="My Appointments", bg=CLR_BG, fg=CLR_TEXT, font=FONT_H1).pack(side=tk.LEFT)
        tk.Button(hdr, text="＋  Book New", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", padx=14, pady=7,
                  activebackground="#1558b0", activeforeground=CLR_WHITE,
                  command=self._book_appointment_dialog).pack(side=tk.RIGHT)

        tab_frame = tk.Frame(inner, bg=CLR_BG)
        tab_frame.pack(fill=tk.X, padx=28, pady=(0, 8))
        self._tab_bar(tab_frame, ["Upcoming", "Past", "Cancelled"], lambda t: None)

        card = tk.Frame(inner, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
        card.pack(fill=tk.X, padx=28, pady=(0, 24))

        col_frame = tk.Frame(card, bg=CLR_BG, pady=8)
        col_frame.pack(fill=tk.X, padx=14)
        for h, w in zip(["Doctor", "Department", "Date", "Time", "Status"], [20, 16, 14, 12, 12]):
            tk.Label(col_frame, text=h, width=w, bg=CLR_BG, fg=CLR_MUTED, font=("Segoe UI", 9, "bold"), anchor=tk.W).pack(side=tk.LEFT, padx=4)

        empty = tk.Frame(card, bg=CLR_WHITE, pady=40)
        empty.pack(fill=tk.X)
        tk.Label(empty, text="📭", bg=CLR_WHITE, font=("Segoe UI Emoji", 36)).pack()
        tk.Label(empty, text="No appointments found", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_BODY).pack(pady=(8, 4))
        tk.Label(empty, text="Your booked appointments will appear here.", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack()
        tk.Button(empty, text="＋  Book Appointment", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", padx=14, pady=7,
                  activebackground="#1558b0", activeforeground=CLR_WHITE,
                  command=self._book_appointment_dialog).pack(pady=(14, 0))
        tk.Frame(card, bg=CLR_WHITE, height=16).pack()

    def _build_medical_records_page(self, parent):
        inner = self._scrollable(parent)

        hdr = tk.Frame(inner, bg=CLR_BG)
        hdr.pack(fill=tk.X, padx=28, pady=(24, 14))
        tk.Label(hdr, text="Medical Records", bg=CLR_BG, fg=CLR_TEXT, font=FONT_H1).pack(side=tk.LEFT)

        tab_frame = tk.Frame(inner, bg=CLR_BG)
        tab_frame.pack(fill=tk.X, padx=28, pady=(0, 8))
        self._tab_bar(tab_frame, ["Diagnoses", "Prescriptions", "Lab Reports", "Documents"], lambda t: None)

        sections = [
            ("🩺", "Diagnoses",     "No diagnoses recorded yet."),
            ("💊", "Prescriptions", "No active prescriptions."),
            ("🧪", "Lab Reports",   "No lab reports uploaded."),
            ("📄", "Documents",     "No documents attached."),
        ]
        for icon, title, empty_msg in sections:
            card = tk.Frame(inner, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
            card.pack(fill=tk.X, padx=28, pady=(0, 14))

            card_hdr = tk.Frame(card, bg=CLR_WHITE, pady=12)
            card_hdr.pack(fill=tk.X, padx=18)
            tk.Label(card_hdr, text=f"{icon}  {title}", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(side=tk.LEFT)

            empty = tk.Frame(card, bg=CLR_WHITE, pady=22)
            empty.pack(fill=tk.X)
            tk.Label(empty, text=empty_msg, bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_BODY).pack()
            tk.Frame(card, bg=CLR_WHITE, height=10).pack()

    def _build_profile_page(self, parent):
        inner = self._scrollable(parent)

        tk.Label(inner, text="My Profile", bg=CLR_BG, fg=CLR_TEXT, font=FONT_H1).pack(anchor=tk.W, padx=28, pady=(24, 14))

        cols = tk.Frame(inner, bg=CLR_BG)
        cols.pack(fill=tk.X, padx=28, pady=(0, 24))
        cols.columnconfigure(0, weight=2)
        cols.columnconfigure(1, weight=3)

        left = tk.Frame(cols, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
        left.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 14))

        avatar_wrap = tk.Frame(left, bg=CLR_WHITE, pady=28)
        avatar_wrap.pack()
        av = tk.Frame(avatar_wrap, bg=CLR_PRIMARY, width=90, height=90)
        av.pack()
        av.pack_propagate(False)
        tk.Label(av, text="👤", bg=CLR_PRIMARY, font=("Segoe UI Emoji", 40)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(left, text=self.patient["name"], bg=CLR_WHITE, fg=CLR_TEXT, font=("Segoe UI", 13, "bold")).pack()
        tk.Label(left, text=self.patient["id"], bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack(pady=(2, 0))
        tk.Label(left, text=f"Member since {self.patient['joined']}", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack(pady=(2, 0))

        tk.Frame(left, bg=CLR_BORDER, height=1).pack(fill=tk.X, padx=18, pady=14)

        for lbl_text, val in [
            ("Blood Type", self.patient["blood"]),
            ("Age",        str(self.patient["age"]) + " years"),
            ("Gender",     self.patient["gender"])
        ]:
            row = tk.Frame(left, bg=CLR_WHITE)
            row.pack(fill=tk.X, padx=18, pady=3)
            tk.Label(row, text=lbl_text + ":", bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL, width=12, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=val, bg=CLR_WHITE, fg=CLR_TEXT, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        tk.Frame(left, bg=CLR_WHITE, height=18).pack()

        right = tk.Frame(cols, bg=CLR_WHITE, highlightbackground=CLR_BORDER, highlightthickness=1)
        right.grid(row=0, column=1, sticky=tk.NSEW)

        tk.Label(right, text="Personal Information", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(anchor=tk.W, padx=20, pady=(18, 10))
        tk.Frame(right, bg=CLR_BORDER, height=1).pack(fill=tk.X, padx=20)

        fields = [
            ("Full Name",         self.patient["name"]),
            ("Phone Number",      self.patient["phone"]),
            ("Email Address",     self.patient["email"]),
            ("Address",           self.patient["address"]),
            ("Date of Birth",     ""),
            ("Emergency Contact", ""),
        ]
        form = tk.Frame(right, bg=CLR_WHITE, padx=20, pady=12)
        form.pack(fill=tk.X)

        for field_label, default in fields:
            tk.Label(form, text=field_label, bg=CLR_WHITE, fg=CLR_TEXT, font=("Segoe UI", 9, "bold"), anchor=tk.W).pack(anchor=tk.W, pady=(8, 2))
            ef = tk.Frame(form, bg=CLR_BORDER, padx=1, pady=1)
            ef.pack(fill=tk.X)
            e = tk.Entry(ef, font=FONT_BODY, bd=0, bg=CLR_WHITE, fg=CLR_TEXT, insertbackground=CLR_TEXT)
            e.insert(0, default)
            e.pack(fill=tk.X, padx=10, pady=7)

        tk.Button(form, text="💾  Save Changes", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", padx=16, pady=8,
                  activebackground="#1558b0", activeforeground=CLR_WHITE,
                  command=lambda: messagebox.showinfo("HOPIFY", "✅ Profile updated successfully!")).pack(anchor=tk.E, pady=(14, 0))
        tk.Frame(right, bg=CLR_WHITE, height=16).pack()

    def _tab_bar(self, parent, tabs, on_select):
        active_tab = tk.StringVar(value=tabs[0])
        tab_widgets = {}

        def select(t):
            active_tab.set(t)
            for tab, (f, lbl) in tab_widgets.items():
                is_active = (tab == t)
                f.config(bg=CLR_PRIMARY if is_active else CLR_WHITE, highlightbackground=CLR_PRIMARY if is_active else CLR_BORDER)
                lbl.config(bg=CLR_PRIMARY if is_active else CLR_WHITE, fg=CLR_WHITE if is_active else CLR_MUTED,
                           font=("Segoe UI", 9, "bold") if is_active else ("Segoe UI", 9))
            on_select(t)

        for i, tab in enumerate(tabs):
            is_first = (i == 0)
            f = tk.Frame(parent, bg=CLR_PRIMARY if is_first else CLR_WHITE,
                         highlightbackground=CLR_PRIMARY if is_first else CLR_BORDER,
                         highlightthickness=1, cursor="hand2", padx=14, pady=6)
            f.pack(side=tk.LEFT, padx=(0, 6))
            lbl = tk.Label(f, text=tab, bg=CLR_PRIMARY if is_first else CLR_WHITE,
                           fg=CLR_WHITE if is_first else CLR_MUTED,
                           font=("Segoe UI", 9, "bold") if is_first else ("Segoe UI", 9))
            lbl.pack()
            tab_widgets[tab] = (f, lbl)
            for w in [f, lbl]:
                w.bind("<Button-1>", lambda e, t=tab: select(t))

    def _book_appointment_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Book Appointment — HOPIFY")
        dialog.geometry("480x520")
        dialog.resizable(False, False)
        dialog.configure(bg=CLR_WHITE)
        dialog.grab_set()

        x = self.winfo_x() + (self.winfo_width()  - 480) // 2
        y = self.winfo_y() + (self.winfo_height() - 520) // 2
        dialog.geometry(f"480x520+{x}+{y}")

        hdr = tk.Frame(dialog, bg=CLR_PRIMARY, pady=18)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="📅  Book New Appointment", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 13, "bold")).pack(padx=20, anchor=tk.W)
        tk.Label(hdr, text=f"Patient: {self.patient['name']}  ({self.patient['id']})", bg=CLR_PRIMARY, fg="#B8D4FF", font=FONT_SMALL).pack(padx=20, anchor=tk.W)

        form = tk.Frame(dialog, bg=CLR_WHITE, padx=24, pady=16)
        form.pack(fill=tk.BOTH, expand=True)

        fields_placeholders = [
            ("Doctor / Specialist", "e.g. Dr. xxxx"),
            ("Department",          "e.g. Cardiology"),
            ("Preferred Date",      "YYYY-MM-DD"),
            ("Preferred Time",      "e.g. 10:00 AM"),
            ("Reason / Notes",      "Brief description"),
        ]

        entries = []
        for field_label, placeholder in fields_placeholders:
            tk.Label(form, text=field_label, bg=CLR_WHITE, fg=CLR_TEXT, font=("Segoe UI", 9, "bold"), anchor=tk.W).pack(anchor=tk.W, pady=(8, 2))
            ef = tk.Frame(form, bg=CLR_BORDER, padx=1, pady=1)
            ef.pack(fill=tk.X)
            e = tk.Entry(ef, font=FONT_BODY, bd=0, bg=CLR_WHITE, fg=CLR_MUTED, insertbackground=CLR_TEXT)
            e.insert(0, placeholder)
            e.pack(fill=tk.X, padx=10, pady=7)

            def on_focus_in(event, ent=e, ph=placeholder):
                if ent.get() == ph:
                    ent.delete(0, tk.END)
                    ent.config(fg=CLR_TEXT)

            def on_focus_out(event, ent=e, ph=placeholder):
                if ent.get().strip() == "":
                    ent.insert(0, ph)
                    ent.config(fg=CLR_MUTED)

            e.bind("<FocusIn>",  on_focus_in)
            e.bind("<FocusOut>", on_focus_out)
            entries.append((field_label, e, placeholder))

        def submit():
            messagebox.showinfo("HOPIFY", "✅ Appointment request submitted!\n\nYou will be notified once confirmed.", parent=dialog)
            dialog.destroy()

        btn_frame = tk.Frame(form, bg=CLR_WHITE)
        btn_frame.pack(fill=tk.X, pady=(16, 0))
        tk.Button(btn_frame, text="Cancel", bg=CLR_BG, fg=CLR_MUTED, font=FONT_BODY, relief=tk.FLAT,
                  padx=14, pady=8, cursor="hand2", command=dialog.destroy).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="✔  Submit Request", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, padx=16, pady=8, cursor="hand2",
                  activebackground="#1558b0", activeforeground=CLR_WHITE,
                  command=submit).pack(side=tk.RIGHT)


if __name__ == "__main__":
    if not USE_BOOTSTRAP:
        print("ttkbootstrap not found — running with plain tkinter.")
    app = PatientDashboard()
    app.mainloop()