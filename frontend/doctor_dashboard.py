import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tbs
from ttkbootstrap.constants import *
import datetime
import subprocess, os, sys

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DoctorDashboard(tbs.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(themename="darkly", *args, **kwargs)

        self.pages = {}
        self.title("Hopify — Doctor Dashboard")
        self.geometry("1280x800")
        self.minsize(1050, 680)
        self.configure(bg=BG_DARK)

        self.doctor = {
            "name":           "Dr. Aawesh Bhattarai",
            "id":             "DC-07-07",
            "specialization": "Cardiology",
            "department":     "Cardiology",
            "qualification":  "MBBS, MD (Cardiology)",
            "phone":          "+977-9709028064",
            "email":          "aawesh_bhattarai@hopify.np",
            "address":        "Itahari, Sunsari",
            "joined":         "05 May 2026",
            "room":           "OPD-12",
            "schedule":       "Sun – Thu   09:00 – 17:00",
        }

        self.appointments = [
            {"time": "09:00 AM", "patient": "Diwakar Sharma",  "id": "PT-11-23", "type": "Follow-up",    "status": "Confirmed", "age": 34},
            {"time": "10:00 AM", "patient": "Pratik Fuyal",   "id": "PT-11-24", "type": "Consultation", "status": "Confirmed", "age": 27},
            {"time": "11:00 AM", "patient": "Sumit Kr. Shah",  "id": "PT-11-25", "type": "Check-up",     "status": "Pending",   "age": 45},
            {"time": "02:00 PM", "patient": "Lucky Ali",       "id": "PT-11-26", "type": "Consultation", "status": "Confirmed", "age": 31},
            {"time": "03:30 PM", "patient": "Aarush Thapa",    "id": "PT-11-27", "type": "Follow-up",    "status": "Pending",   "age": 58},
        ]

        self.patients = [
            {"name": "Diwakar Sharma", "id": "PT-11-23", "age": 34, "blood": "O+",  "last_visit": "15 May 2025", "condition": "Hernia, Penile Disfunction"},
            {"name": "Pratik Fuyal",  "id": "PT-11-24", "age": 27, "blood": "A+",  "last_visit": "10 May 2025", "condition": "Arrhythmia"},
            {"name": "Sumit Kr. Shah", "id": "PT-11-25", "age": 45, "blood": "B+",  "last_visit": "08 May 2025", "condition": "Coronary Artery Disease"},
            {"name": "Lucky Ali",      "id": "PT-11-26", "age": 31, "blood": "AB−", "last_visit": "02 May 2025", "condition": "Palpitations"},
            {"name": "Aarush Thapa",   "id": "PT-11-27", "age": 58, "blood": "O−",  "last_visit": "28 Apr 2025", "condition": "Heart Failure"},
        ]

        self.active_nav   = tk.StringVar(value="Dashboard")
        self._nav_buttons = {}
        self._active_canvas = None

        self._build_ui()
        self._center_window()
        self._show_page("Dashboard")

    # ── Window helpers ────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = 1280, 800
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _on_mousewheel(self, event):
        if self._active_canvas:
            self._active_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Layout ────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.bind("<MouseWheel>", self._on_mousewheel)

        root_frame = tk.Frame(self, bg=BG_DARK)
        root_frame.pack(fill=BOTH, expand=True)

        self._build_sidebar(root_frame).pack(side=LEFT, fill=Y)

        self.main = tk.Frame(root_frame, bg=BG_MAIN)
        self.main.pack(side=LEFT, fill=BOTH, expand=True)

        self._build_topbar(self.main)
        self.page_container = tk.Frame(self.main, bg=BG_MAIN)
        self.page_container.pack(fill=BOTH, expand=True, padx=24, pady=20)

    # ── Sidebar ───────────────────────────────────────────────────────────

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG_SIDEBAR, width=230)
        sb.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(sb, bg=BG_SIDEBAR, pady=24)
        logo_frame.pack(fill=X, padx=18)
        tk.Label(logo_frame, text="HOPIFY", bg=BG_SIDEBAR,
                 fg=WHITE, font=FONT_LOGO).pack(side=LEFT)

        tk.Label(sb, text="Doctor Portal", bg=BG_SIDEBAR,
                 fg=TEXT_HINT, font=FONT_SMALL).pack(anchor=W, padx=22, pady=(0, 14))

        self._sidebar_divider(sb)

        nav_items = [
            ("Dashboard",       "›"),
            ("Appointments",    "›"),
            ("My Patients",     "›"),
            ("Prescriptions",   "›"),
            ("Medical Records", "›"),
            ("My Profile",      "›"),
            ("Settings",        "›"),
        ]
        for label, arrow in nav_items:
            self._nav_item(sb, label)

        tk.Frame(sb, bg=BG_SIDEBAR).pack(fill=Y, expand=True)
        self._sidebar_divider(sb)

        # User card
        user_frame = tk.Frame(sb, bg=SB_HOVER, padx=14, pady=10)
        user_frame.pack(fill=X, padx=10, pady=10)

        # Avatar initial circle
        av = tk.Frame(user_frame, bg=ACCENT, width=36, height=36)
        av.pack(side=LEFT, padx=(0, 10))
        av.pack_propagate(False)
        initials = "".join(p[0].upper() for p in self.doctor["name"].split()
                           if p and p[0].isalpha())[:2]
        tk.Label(av, text=initials, bg=ACCENT, fg=WHITE,
                 font=("Segoe UI", 11, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)

        info = tk.Frame(user_frame, bg=SB_HOVER)
        info.pack(side=LEFT)
        tk.Label(info, text=self.doctor["name"], bg=SB_HOVER,
                 fg=TEXT_MAIN, font=("Segoe UI", 9, "bold")).pack(anchor=W)
        tk.Label(info, text=self.doctor["specialization"], bg=SB_HOVER,
                 fg=TEXT_HINT, font=FONT_SMALL).pack(anchor=W)

        self._nav_item(sb, "Logout", danger=True)
        return sb

    def _sidebar_divider(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=X, padx=14, pady=6)

    def _nav_item(self, parent, label, danger=False):
        fg_default = DANGER if danger else TEXT_SUB
        bg_default = BG_SIDEBAR

        frame = tk.Frame(parent, bg=bg_default, cursor="hand2", padx=16, pady=9)
        frame.pack(fill=X, padx=6, pady=1)

        text_lbl = tk.Label(frame, text=label, bg=bg_default,
                            fg=fg_default, font=FONT_NAV, anchor=W)
        text_lbl.pack(side=LEFT, fill=X, expand=True)

        accent_bar = tk.Frame(frame, bg=ACCENT, width=3)

        self._nav_buttons[label] = (frame, text_lbl, accent_bar)

        for w in [frame, text_lbl]:
            w.bind("<Button-1>", lambda e, lbl=label: self.set_active(lbl))
            w.bind("<Enter>", lambda e, f=frame, t=text_lbl, lbl=label:
                   (f.config(bg=SB_HOVER), t.config(bg=SB_HOVER))
                   if lbl != self.active_nav.get() else None)
            w.bind("<Leave>", lambda e, f=frame, t=text_lbl, lbl=label:
                   (f.config(bg=bg_default), t.config(bg=bg_default))
                   if lbl != self.active_nav.get() else None)

        if label == "Dashboard":
            self._highlight_nav(label)

    def _highlight_nav(self, label):
        frame, text_lbl, accent_bar = self._nav_buttons[label]
        frame.config(bg=SB_ACTIVE)
        text_lbl.config(bg=SB_ACTIVE, fg=WHITE, font=("Segoe UI", 10, "bold"))
        accent_bar.pack(side=RIGHT, fill=Y)

    def _unhighlight_nav(self, label):
        frame, text_lbl, accent_bar = self._nav_buttons[label]
        is_danger = (label == "Logout")
        frame.config(bg=BG_SIDEBAR)
        text_lbl.config(bg=BG_SIDEBAR,
                        fg=DANGER if is_danger else TEXT_SUB,
                        font=FONT_NAV)
        accent_bar.pack_forget()

    def set_active(self, lbl):
        if lbl == "Logout":
            if messagebox.askyesno("Hopify", "Are you sure you want to logout?"):
                app.destroy()
                subprocess.Popen([sys.executable,
                                  os.path.join(BASE_DIR, "login_page.py")])
            return

        for btn_lbl in self._nav_buttons:
            self._unhighlight_nav(btn_lbl)

        self._highlight_nav(lbl)
        self.active_nav.set(lbl)
        self._show_page(lbl)

    # ── Topbar ────────────────────────────────────────────────────────────

    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=BG_CARD, pady=14)
        bar.pack(fill=X)
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=X)

        left = tk.Frame(bar, bg=BG_CARD)
        left.pack(side=LEFT, padx=28)
        self.topbar_title = tk.Label(left, text="Dashboard", bg=BG_CARD,
                                      fg=TEXT_MAIN, font=FONT_H1)
        self.topbar_title.pack(anchor=W)
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        tk.Label(left, text=today, bg=BG_CARD, fg=TEXT_HINT,
                 font=FONT_SMALL).pack(anchor=W)

        right = tk.Frame(bar, bg=BG_CARD)
        right.pack(side=RIGHT, padx=28)

        self._topbar_btn(right, "Add Prescription", SUCCESS,
                         "#1aad8a", self._add_prescription_dialog, side=LEFT)
        tk.Frame(right, bg=BG_CARD, width=10).pack(side=LEFT)
        self._topbar_btn(right, "Manage Schedule", ACCENT,
                         ACCENT2, self._manage_schedule_dialog, side=LEFT)

    def _topbar_btn(self, parent, text, bg, hover_bg, cmd, side=LEFT):
        btn = tk.Button(parent, text=text, bg=bg, fg=WHITE,
                        font=("Segoe UI", 10, "bold"), relief=FLAT,
                        cursor="hand2", padx=14, pady=7,
                        activebackground=hover_bg, activeforeground=WHITE,
                        bd=0, command=cmd)
        btn.pack(side=side)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    # ── Page routing ──────────────────────────────────────────────────────

    def _show_page(self, page_name):
        self.topbar_title.config(text=page_name)
        for child in self.page_container.winfo_children():
            child.destroy()
        self._active_canvas = None

        if page_name == "Dashboard":
            self._render_dashboard()
        elif page_name == "Appointments":
            self._render_appointments()
        elif page_name == "My Patients":
            self._render_patients()
        elif page_name == "My Profile":
            self._render_profile()
        else:
            self._render_placeholder(page_name)

    def _render_placeholder(self, name):
        frame = tk.Frame(self.page_container, bg=BG_CARD,
                         highlightbackground=BORDER, highlightthickness=1,
                         padx=30, pady=40)
        frame.pack(fill=BOTH, expand=True)
        tk.Label(frame, text=name, bg=BG_CARD, fg=TEXT_MAIN, font=FONT_H1).pack()
        tk.Label(frame, text="This section is under development.",
                 bg=BG_CARD, fg=TEXT_HINT, font=FONT_BODY).pack(pady=(8, 0))

    # ── Scrollable helper ─────────────────────────────────────────────────

    def _scrollable(self, parent):
        canvas = tk.Canvas(parent, bg=BG_MAIN, highlightthickness=0)
        sb = ttk.Scrollbar(parent, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self._active_canvas = canvas

        inner = tk.Frame(canvas, bg=BG_MAIN)
        win = canvas.create_window((0, 0), window=inner, anchor=NW)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",
            lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        return inner

    # ── Card helper ───────────────────────────────────────────────────────

    def _card(self, parent, **pack_kw):
        c = tk.Frame(parent, bg=BG_CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        c.pack(**pack_kw)
        return c

    def _section_header(self, parent, text, btn_text=None, btn_cmd=None):
        row = tk.Frame(parent, bg=BG_CARD, pady=14)
        row.pack(fill=X, padx=20)
        tk.Label(row, text=text, bg=BG_CARD, fg=TEXT_MAIN,
                 font=FONT_H2).pack(side=LEFT)
        if btn_text:
            b = tk.Label(row, text=btn_text, bg=BG_CARD, fg=ACCENT2,
                         font=("Segoe UI", 9), cursor="hand2")
            b.pack(side=RIGHT)
            b.bind("<Button-1>", lambda e: btn_cmd())
        tk.Frame(parent, bg=BORDER, height=1).pack(fill=X, padx=20)

    # ── Treeview helper ───────────────────────────────────────────────────

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

        tree = ttk.Treeview(parent, columns=columns, show="headings",
                            style="Dark.Treeview")
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
        if col_widths:
            for col, w in zip(columns, col_widths):
                tree.column(col, width=w, anchor=CENTER if w < 180 else W)
        tree.pack(fill=BOTH, expand=True, padx=20, pady=(10, 16))
        return tree

    # ── Dashboard ─────────────────────────────────────────────────────────

    def _render_dashboard(self):
        inner = self._scrollable(self.page_container)

        # Stat cards
        stats_row = tk.Frame(inner, bg=BG_MAIN)
        stats_row.pack(fill=X, pady=(0, 20))

        stats = [
            ("Today's Appointments", str(len(self.appointments)), ACCENT),
            ("Patients on Roster",   str(len(self.patients)),     SUCCESS),
            ("Assigned Ward",        self.doctor["room"],         WARNING),
        ]
        for i, (title, val, color) in enumerate(stats):
            card = tk.Frame(stats_row, bg=BG_CARD,
                            highlightbackground=BORDER, highlightthickness=1,
                            padx=20, pady=16)
            card.pack(side=LEFT, fill=X, expand=True,
                      padx=(0 if i == 0 else 14, 0))

            accent_bar = tk.Frame(card, bg=color, width=4)
            accent_bar.pack(side=LEFT, fill=Y, padx=(0, 16))

            body = tk.Frame(card, bg=BG_CARD)
            body.pack(side=LEFT, fill=BOTH, expand=True)

            tk.Label(body, text=title, bg=BG_CARD,
                     fg=TEXT_HINT, font=FONT_SMALL).pack(anchor=W)
            tk.Label(body, text=val, bg=BG_CARD,
                     fg=TEXT_MAIN, font=FONT_STAT).pack(anchor=W)

        # Appointment table
        card = self._card(inner, fill=BOTH, expand=True)
        self._section_header(card, "Today's Appointment Queue")

        tree = self._styled_tree(
            card,
            columns=("time", "patient", "type", "status"),
            headings=("Time", "Patient", "Type", "Status"),
            col_widths=[110, 260, 140, 120],
        )
        for appt in self.appointments:
            tree.insert("", END, values=(
                appt["time"], appt["patient"],
                appt["type"], appt["status"]))

    # ── Appointments ──────────────────────────────────────────────────────

    def _render_appointments(self):
        card = self._card(self.page_container, fill=BOTH, expand=True)
        self._section_header(card, "All Appointments")

        tree = self._styled_tree(
            card,
            columns=("time", "id", "patient", "age", "type", "status"),
            headings=("Time", "Patient ID", "Patient", "Age", "Type", "Status"),
            col_widths=[110, 110, 220, 60, 130, 110],
        )
        for appt in self.appointments:
            tree.insert("", END, values=(
                appt["time"], appt["id"], appt["patient"],
                appt["age"], appt["type"], appt["status"]))

    # ── Patients ──────────────────────────────────────────────────────────

    def _render_patients(self):
        card = self._card(self.page_container, fill=BOTH, expand=True)
        self._section_header(card, "Patient Roster")

        tree = self._styled_tree(
            card,
            columns=("id", "name", "age", "blood", "condition", "last_visit"),
            headings=("ID", "Patient Name", "Age", "Blood", "Condition", "Last Visit"),
            col_widths=[110, 200, 60, 80, 220, 130],
        )
        for pat in self.patients:
            tree.insert("", END, values=(
                pat["id"], pat["name"], pat["age"],
                pat["blood"], pat["condition"], pat["last_visit"]))

    # ── Profile ───────────────────────────────────────────────────────────

    def _render_profile(self):
        card = self._card(self.page_container, fill=BOTH, expand=True)
        self._section_header(card, "My Profile")

        body = tk.Frame(card, bg=BG_CARD, padx=28, pady=20)
        body.pack(fill=BOTH, expand=True)

        details = [
            ("Full Name",        self.doctor["name"]),
            ("Doctor ID",        self.doctor["id"]),
            ("Specialization",   self.doctor["specialization"]),
            ("Department",       self.doctor["department"]),
            ("Qualification",    self.doctor["qualification"]),
            ("Room / Ward",      self.doctor["room"]),
            ("Working Hours",    self.doctor["schedule"]),
            ("Phone",            self.doctor["phone"]),
            ("Email",            self.doctor["email"]),
            ("Address",          self.doctor["address"]),
        ]

        for i, (lbl_text, val_text) in enumerate(details):
            row = tk.Frame(body, bg=BG_CARD)
            row.pack(fill=X, pady=5)
            tk.Frame(row, bg=BORDER, height=1).pack(fill=X) if i else None

            tk.Label(row, text=lbl_text, bg=BG_CARD, fg=TEXT_HINT,
                     font=FONT_LABEL, width=20, anchor=W).pack(side=LEFT, pady=6)
            tk.Label(row, text=val_text, bg=BG_CARD, fg=TEXT_MAIN,
                     font=FONT_BODY, anchor=W).pack(side=LEFT, pady=6)

    # ── Dialogs ───────────────────────────────────────────────────────────

    def _add_prescription_dialog(self):
        messagebox.showinfo("Hopify", "Prescription module coming soon.")

    def _manage_schedule_dialog(self):
        messagebox.showinfo("Hopify", "Schedule management coming soon.")


if __name__ == "__main__":
    app = DoctorDashboard()
    app.mainloop()
