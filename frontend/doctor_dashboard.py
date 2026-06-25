//a
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tbs
from ttkbootstrap.constants import *
import datetime
import subprocess, os, sys

CLR_SIDEBAR    = "#2563B0"
CLR_SIDEBAR_LT = "#3074C2"
CLR_PRIMARY    = "#1A73E8"
CLR_ACCENT     = "#00C9A7"
CLR_BG         = "#F4F7FE"
CLR_WHITE      = "#FFFFFF"
CLR_TEXT       = "#1E2A3A"
CLR_MUTED      = "#6B7A99"
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DoctorDashboard(tbs.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(themename="litera", *args, **kwargs)
        
        self.pages = {}  
    
        self.title("HOPIFY — Doctor Dashboard")
        self.geometry("1280x800")
        self.minsize(1050, 680)
        self.configure(bg=CLR_BG)

        self.doctor = {
            "name":          "Dr. Aawesh Bhattarai",
            "id":            "dc-07-07",
            "specialization":"cardiology",
            "department":    "cardiology",
            "qualification": "MBBS, MD (cardiology)",
            "phone":         "+977-9709028064",
            "email":         "aawehs_bhattarai@hopify.np",
            "address":       "itahari,sunsari",
            "joined":        "05 May 2026",
            "room":          "OPD-12",
            "schedule":      "Sun-Thu  09:00-17:00",
        }

        self.appointments = [
            {"time": "09:00 AM", "patient": "Diwakar sharma",  "id": "pt-11-23", "type": "Follow-up",    "status": "Confirmed",  "age": 34},
            {"time": "10:00 AM", "patient": "Pratik phuyal",      "id": "pt-11-24", "type": "Consultation", "status": "Confirmed",  "age": 27},
            {"time": "11:00 AM", "patient": "sumit kr.shah",       "id": "pt-11-25", "type": "Check-up",     "status": "Pending",    "age": 45},
            {"time": "02:00 PM", "patient": "lucky Ali",      "id": "pt-11-26", "type": "Consultation", "status": "Confirmed",  "age": 31},
            {"time": "03:30 PM", "patient": "Aarush Thapa",        "id": "pt-11-27", "type": "Follow-up",    "status": "Pending",    "age": 58},
        ]

        self.patients = [
            {"name": "Diwakar sharma", "id": "pt-11-23", "age": 34, "blood": "O+",  "last_visit": "15 May 2025", "condition": "Hypertension"},
            {"name": "Pratik phuyal",     "id": "pt-11-24", "age": 27, "blood": "A+",  "last_visit": "10 May 2025", "condition": "Arrhythmia"},
            {"name": "sumit kr.shah",      "id": "pt-11-25", "age": 45, "blood": "B+",  "last_visit": "08 May 2025", "condition": "Coronary Artery Disease"},
            {"name": "lucky Ali",     "id": "pt-11-26", "age": 31, "blood": "AB-", "last_visit": "02 May 2025", "condition": "Palpitations"},
            {"name": "Aarush Thapa",       "id": "pt-11-27", "age": 58, "blood": "O-",  "last_visit": "28 Apr 2025", "condition": "Heart Failure"},
        ]

        self.active_nav   = tk.StringVar(value="Dashboard")
        self._nav_buttons = {}
        self._active_canvas = None
        
        self._build_ui()
        self._center_window()
        self._show_page("Dashboard")

    def _center_window(self):
        self.update_idletasks()
        w, h = 1280, 800
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _on_mousewheel(self, event):
        if self._active_canvas:
            self._active_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_ui(self):
        self.bind("<MouseWheel>", self._on_mousewheel)

        root_frame = tk.Frame(self, bg=CLR_BG)
        root_frame.pack(fill=BOTH, expand=True)

        self.sidebar = self._build_sidebar(root_frame)
        self.sidebar.pack(side=LEFT, fill=Y)

        self.main = tk.Frame(root_frame, bg=CLR_BG)
        self.main.pack(side=LEFT, fill=BOTH, expand=True)

        self._build_topbar(self.main)
        self.page_container = tk.Frame(self.main, bg=CLR_BG)
        self.page_container.pack(fill=BOTH, expand=True, padx=24, pady=20)

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=CLR_SIDEBAR, width=230)
        sb.pack_propagate(False)

        logo_frame = tk.Frame(sb, bg=CLR_SIDEBAR, pady=22)
        logo_frame.pack(fill=X, padx=18)
        tk.Label(logo_frame, text="🏥", bg=CLR_SIDEBAR, font=("Segoe UI Emoji", 22)).pack(side=LEFT)
        tk.Label(logo_frame, text=" HOPIFY", bg=CLR_SIDEBAR, fg=CLR_WHITE, font=FONT_LOGO).pack(side=LEFT)

        tk.Label(sb, text="Doctor Portal", bg=CLR_SIDEBAR, fg="#A0BEE0", font=FONT_SMALL).pack(anchor=W, padx=22, pady=(0, 14))

        self._sidebar_divider(sb)

        nav_items = [
            ("📊", "Dashboard"),
            ("📅", "Appointments"),
            ("👥", "My Patients"),
            ("📋", "Prescriptions"),
            ("📝", "Medical Records"),
            ("👤", "My Profile"),
            ("⚙️", "Settings"),
        ]
        for icon, label in nav_items:
            self._nav_item(sb, icon, label)

        tk.Frame(sb, bg=CLR_SIDEBAR).pack(fill=Y, expand=True)
        self._sidebar_divider(sb)

        user_frame = tk.Frame(sb, bg=CLR_SIDEBAR_LT, padx=14, pady=10)
        user_frame.pack(fill=X, padx=10, pady=10)
        tk.Label(user_frame, text="👨‍⚕️", bg=CLR_SIDEBAR_LT, font=("Segoe UI Emoji", 18)).pack(side=LEFT, padx=(0, 8))
        
        info = tk.Frame(user_frame, bg=CLR_SIDEBAR_LT)
        info.pack(side=LEFT)
        tk.Label(info, text=self.doctor["name"], bg=CLR_SIDEBAR_LT, fg=CLR_WHITE, font=("Segoe UI", 10, "bold")).pack(anchor=W)
        tk.Label(info, text=self.doctor["specialization"].title(), bg=CLR_SIDEBAR_LT, fg="#A0BEE0", font=FONT_SMALL).pack(anchor=W)

        self._nav_item(sb, "🚪", "Logout")
        return sb

    def _sidebar_divider(self, parent):
        tk.Frame(parent, bg="#4A90D9", height=1).pack(fill=X, padx=14, pady=6)

    def _nav_item(self, parent, icon, label):
        is_logout = label == "Logout"
        frame = tk.Frame(parent, bg=CLR_SIDEBAR, cursor="hand2", padx=14, pady=8)
        frame.pack(fill=X, padx=8, pady=1)

        icon_lbl = tk.Label(frame, text=icon, bg=CLR_SIDEBAR, fg=CLR_WHITE, font=("Segoe UI Emoji", 13))
        icon_lbl.pack(side=LEFT, padx=(0, 10))

        text_lbl = tk.Label(frame, text=label, bg=CLR_SIDEBAR, fg="#C8D8F0" if not is_logout else "#EF8080", font=FONT_NAV, anchor=W)
        text_lbl.pack(side=LEFT, fill=X)

        accent = tk.Frame(frame, bg=CLR_ACCENT, width=4)

        self._nav_buttons[label] = (frame, text_lbl, icon_lbl, accent)

        for w in [frame, icon_lbl, text_lbl]:
            w.bind("<Button-1>", lambda e, label_name=label: self.set_active(label_name))
            w.bind("<Enter>", lambda e, f=frame, t=text_lbl, i=icon_lbl, lbl=label: 
                   (f.config(bg="#2E72C2"), t.config(bg="#2E72C2"), i.config(bg="#2E72C2")) if lbl != self.active_nav.get() else None)
            w.bind("<Leave>", lambda e, f=frame, t=text_lbl, i=icon_lbl, lbl=label: 
                   (f.config(bg=CLR_SIDEBAR), t.config(bg=CLR_SIDEBAR), i.config(bg=CLR_SIDEBAR)) if lbl != self.active_nav.get() else None)

        if label == "Dashboard":
            frame.config(bg="#3D85D0")
            text_lbl.config(bg="#3D85D0", fg=CLR_WHITE, font=("Segoe UI", 11, "bold"))
            icon_lbl.config(bg="#3D85D0")
            accent.pack(side=LEFT, fill=Y, padx=(4, 0))

    def set_active(self, lbl):
        if lbl == "Logout":
            if messagebox.askyesno("HOPIFY", "Are you sure you want to logout?"):
                app.destroy()
                subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "login_page.py")])
            return

        for btn_lbl, (btn_f, btn_t, btn_i, btn_a) in self._nav_buttons.items():
            btn_f.config(bg=CLR_SIDEBAR)
            btn_t.config(bg=CLR_SIDEBAR, fg="#C8D8F0" if btn_lbl != "Logout" else "#EF8080", font=FONT_NAV)
            btn_i.config(bg=CLR_SIDEBAR)
            btn_a.pack_forget()

        frame, text_lbl, icon_lbl, accent = self._nav_buttons[lbl]
        frame.config(bg="#3D85D0")
        text_lbl.config(bg="#3D85D0", fg=CLR_WHITE, font=("Segoe UI", 11, "bold"))
        icon_lbl.config(bg="#3D85D0")
        accent.pack(side=LEFT, fill=Y, padx=(4, 0))
        
        self.active_nav.set(lbl)
        self._show_page(lbl)

    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=CLR_WHITE, pady=12)
        bar.pack(fill=X)
        tk.Frame(parent, bg=CLR_BORDER, height=1).pack(fill=X)

        left = tk.Frame(bar, bg=CLR_WHITE)
        left.pack(side=LEFT, padx=24)
        self.topbar_title = tk.Label(left, text="Doctor Dashboard", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H1)
        self.topbar_title.pack(anchor=W)
        
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        tk.Label(left, text=today, bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack(anchor=W)

        right = tk.Frame(bar, bg=CLR_WHITE)
        right.pack(side=RIGHT, padx=24)

        tk.Button(right, text="Add Prescription", bg=CLR_ACCENT, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"), 
                  relief=FLAT, cursor="hand2", padx=14, pady=7, activebackground="#00a88e", activeforeground=CLR_WHITE, 
                  command=self._add_prescription_dialog).pack(side=LEFT, padx=(0, 10))

        tk.Button(right, text="Manage Schedule", bg=CLR_PRIMARY, fg=CLR_WHITE, font=("Segoe UI", 10, "bold"), 
                  relief=FLAT, cursor="hand2", padx=14, pady=7, activebackground="#204474", activeforeground=CLR_WHITE, 
                  command=self._manage_schedule_dialog).pack(side=LEFT)

    def _show_page(self, page_name):
        self.topbar_title.config(text=f"{page_name}")

        for child in self.page_container.winfo_children():
            child.destroy()

        if page_name == "Dashboard":
            self._render_dashboard()
        elif page_name == "Appointments":
            self._render_appointments()
        elif page_name == "My Patients":
            self._render_patients()
        elif page_name == "My Profile":
            self._render_profile()
        else:
            placeholder = tk.Frame(self.page_container, bg=CLR_WHITE, bd=1, relief=tk.FLAT, padx=30, pady=30)
            placeholder.pack(fill=BOTH, expand=True)
            tk.Label(placeholder, text=f"📂 {page_name} Module Workspace", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H1).pack(pady=(40, 10))
            tk.Label(placeholder, text=f"Data interface active for subsystem under assignment to {self.doctor['name']}.", 
                     bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_BODY).pack()

    def _render_dashboard(self):
        metrics_frame = tk.Frame(self.page_container, bg=CLR_BG)
        metrics_frame.pack(fill=X, pady=(0, 20))

        stats = [
            ("Active Scheduled Appointments", f"{len(self.appointments)}", CLR_PRIMARY),
            ("Monitored Roster Patients", f"{len(self.patients)}", CLR_ACCENT),
            ("Consultation Ward Assignment", f"{self.doctor['room']}", CLR_WARNING),
        ]

        for i, (title, val, color) in enumerate(stats):
            card = tk.Frame(metrics_frame, bg=CLR_WHITE, bd=0, padx=20, pady=15)
            card.pack(side=LEFT, fill=X, expand=True, padx=(0 if i == 0 else 15, 0))
            
            accent_bar = tk.Frame(card, bg=color, width=5)
            accent_bar.pack(side=LEFT, fill=Y, padx=(0, 15))
            
            body = tk.Frame(card, bg=CLR_WHITE)
            body.pack(side=LEFT, fill=BOTH, expand=True)
            
            tk.Label(body, text=title, bg=CLR_WHITE, fg=CLR_MUTED, font=FONT_SMALL).pack(anchor=W)
            tk.Label(body, text=val, bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_STAT).pack(anchor=W)

        table_container = tk.Frame(self.page_container, bg=CLR_WHITE, bd=0, padx=20, pady=20)
        table_container.pack(fill=BOTH, expand=True)

        tk.Label(table_container, text="Active Queue Timeline View", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(anchor=W, pady=(0, 15))

        columns = ("time", "patient", "type", "status")
        tree = ttk.Treeview(table_container, columns=columns, show="headings", height=8)
        
        tree.heading("time", text="Time Slot")
        tree.heading("patient", text="Patient Name")
        tree.heading("type", text="Visit Classification")
        tree.heading("status", text="Operational Status")

        tree.column("time", width=120, anchor=CENTER)
        tree.column("patient", width=250, anchor=W)
        tree.column("type", width=150, anchor=CENTER)
        tree.column("status", width=150, anchor=CENTER)

        for appt in self.appointments:
            tree.insert("", END, values=(appt["time"], appt["patient"], appt["type"], appt["status"]))

        tree.pack(fill=BOTH, expand=True)

    def _render_appointments(self):
        frame = tk.Frame(self.page_container, bg=CLR_WHITE, padx=20, pady=20)
        frame.pack(fill=BOTH, expand=True)

        tk.Label(frame, text="Consultation Schedule Allocation Management", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(anchor=W, pady=(0, 15))

        columns = ("time", "id", "patient", "age", "type", "status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        tree.heading("time", text="Scheduled Time")
        tree.heading("id", text="Patient Record ID")
        tree.heading("patient", text="Patient Full Name")
        tree.heading("age", text="Age")
        tree.heading("type", text="Appointment Type")
        tree.heading("status", text="Roster Status")

        for appt in self.appointments:
            tree.insert("", END, values=(appt["time"], appt["id"], appt["patient"], appt["age"], appt["type"], appt["status"]))

        tree.pack(fill=BOTH, expand=True)

    def _render_patients(self):
        frame = tk.Frame(self.page_container, bg=CLR_WHITE, padx=20, pady=20)
        frame.pack(fill=BOTH, expand=True)

        tk.Label(frame, text="Assigned Electronic Medical Directory (EMR)", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H2).pack(anchor=W, pady=(0, 15))

        columns = ("id", "name", "age", "blood", "condition", "last_visit")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        tree.heading("id", text="Tracking ID")
        tree.heading("name", text="Patient Legal Name")
        tree.heading("age", text="Age")
        tree.heading("blood", text="Blood Group")
        tree.heading("condition", text="Clinical Assessment Diagnosis")
        tree.heading("last_visit", text="Last Clinical Visit")

        tree.column("blood", width=100, anchor=CENTER)
        tree.column("age", width=80, anchor=CENTER)

        for pat in self.patients:
            tree.insert("", END, values=(pat["id"], pat["name"], pat["age"], pat["blood"], pat["condition"], pat["last_visit"]))

        tree.pack(fill=BOTH, expand=True)

    def _render_profile(self):
        frame = tk.Frame(self.page_container, bg=CLR_WHITE, padx=30, pady=30)
        frame.pack(fill=BOTH, expand=True)

        tk.Label(frame, text="Practitioner Credentials Profile", bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_H1).pack(anchor=W, pady=(0, 20))
        
        details = [
            ("Full Name:", self.doctor["name"]),
            ("Practitioner ID Code:", self.doctor["id"]),
            ("Specialization Track:", self.doctor["specialization"].title()),
            ("Assigned Department:", self.doctor["department"].title()),
            ("Acquired Academic Degree:", self.doctor["qualification"]),
            ("Assigned Workspace Ward:", self.doctor["room"]),
            ("Practice Active Roster Hours:", self.doctor["schedule"]),
            ("Enterprise Telecom Line:", self.doctor["phone"]),
            ("Inbound Clinic Mailbox:", self.doctor["email"]),
            ("Registered Residential Base:", self.doctor["address"].title()),
        ]

        for i, (label_text, value_text) in enumerate(details):
            lbl = tk.Label(frame, text=label_text, bg=CLR_WHITE, fg=CLR_MUTED, font=("Segoe UI", 11, "bold"), width=25, anchor=W)
            lbl.grid(row=i, column=0, pady=8, sticky=W)
            
            val = tk.Label(frame, text=value_text, bg=CLR_WHITE, fg=CLR_TEXT, font=FONT_BODY, anchor=W)
            val.grid(row=i, column=1, pady=8, sticky=W)

    def _add_prescription_dialog(self):
        messagebox.showinfo("Prescription Engine", "Prescription deployment sequence dashboard generated.")

    def _manage_schedule_dialog(self):
        messagebox.showinfo("Schedule Manager", "Doctor clinical timeline settings dialog active.")


if __name__ == "__main__":
    app = DoctorDashboard()
    app.mainloop()
