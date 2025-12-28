import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import webbrowser
import urllib.request
import json
import urllib.parse
import os asdd


def open_url(url):
    webbrowser.open_new(url)


# --- ГЛАВНОЕ ОКНО (создаем в начале, чтобы функции его видели) ---
root = tk.Tk()
root.title("shadPS4 Compatibility Explorer")
root.geometry("650x900")
root.configure(bg="#1e1e1e")

issues_data, links = [], []


def open_registration_window():
    reg_window = tk.Toplevel(root)
    reg_window.title("New Compatibility Report")
    reg_window.geometry("620x980")
    reg_window.configure(bg="#1e1e1e")

    main_frame = tk.Frame(reg_window, bg="#1e1e1e")
    main_frame.pack(fill=tk.BOTH, expand=1, padx=25, pady=15)

    tk.Label(main_frame, text="COMPATIBILITY REPORT FORM", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#00ff00").pack(
        pady=10)

    # ОБЯЗАТЕЛЬНОЕ ПОДТВЕРЖДЕНИЕ
    confirm_var = tk.BooleanVar()
    tk.Checkbutton(main_frame, text="I understand this is a Community list and all data types are accepted *",
                   variable=confirm_var, bg="#1e1e1e", fg="#ffcc00", selectcolor="#1e1e1e",
                   activebackground="#1e1e1e").pack(anchor="w")

    # ВЫБОР: ПИРАТ ИЛИ ДАМП (Нужно выбрать один из двух)
    tk.Label(main_frame, text="\n4. Copy Type (Select one): *", bg="#1e1e1e", fg="#cccccc",
             font=("Arial", 10, "bold")).pack(anchor="w")
    copy_type = tk.StringVar(value="None")

    radio_frame = tk.Frame(main_frame, bg="#2d2d2d", padx=10, pady=5)
    radio_frame.pack(fill=tk.X, pady=5)

    tk.Radiobutton(radio_frame, text="Pirated (Downloaded)", variable=copy_type, value="Pirated",
                   bg="#2d2d2d", fg="white", selectcolor="#007acc").pack(side=tk.LEFT, padx=20)
    tk.Radiobutton(radio_frame, text="Digital Dump (Own)", variable=copy_type, value="Digital Dump (Own)",
                   bg="#2d2d2d", fg="white", selectcolor="#007acc").pack(side=tk.LEFT, padx=20)

    entries = {}

    def create_field(label_text, key, default=""):
        tk.Label(main_frame, text=label_text, bg="#1e1e1e", fg="#cccccc").pack(anchor="w", pady=(10, 0))
        e = tk.Entry(main_frame, width=70, bg="#2d2d2d", fg="white", insertbackground="white", borderwidth=0)
        if default: e.insert(0, default)
        e.pack(pady=5, ipady=3)
        entries[key] = e

    create_field("1. Game Name:", "name")
    create_field("2. Game ID (CUSA):", "id", "CUSA")

    # ВЕРСИЯ И СТАТУС
    tk.Label(main_frame, text="5. shadPS4 Version:", bg="#1e1e1e", fg="#cccccc").pack(anchor="w")
    ver_combo = ttk.Combobox(main_frame, values=["v0.13", "v0.12", "v0.5", "Main Build"], state="readonly")
    ver_combo.set("v0.5")
    ver_combo.pack(pady=5, fill=tk.X)

    tk.Label(main_frame, text="6. Status:", bg="#1e1e1e", fg="#cccccc").pack(anchor="w")
    status_combo = ttk.Combobox(main_frame, values=["Platinum", "Playable", "Orange", "In-Game", "Crashes"],
                                state="readonly")
    status_combo.set("In-Game")
    status_combo.pack(pady=5, fill=tk.X)

    tk.Label(main_frame, text="7. Error Summary:", bg="#1e1e1e", fg="#cccccc").pack(anchor="w")
    error_text = tk.Text(main_frame, width=52, height=5, bg="#2d2d2d", fg="#e0e0e0")
    error_text.pack(pady=5)

    def generate_and_send():
        # ПРОВЕРКИ
        if not confirm_var.get():
            messagebox.showwarning("Warning", "Please confirm the community rules!")
            return
        if copy_type.get() == "None":
            messagebox.showwarning("Warning", "Please select Copy Type: Pirated or Digital Dump!")
            return

        title = f"{entries['id'].get()} - {entries['name'].get()}"
        body = (
            f"- [x] I understand this is a Community list...\n\n"
            f"### Game Name: {entries['name'].get()}\n"
            f"### Game ID: {entries['id'].get()}\n"
            f"### Copy Type: {copy_type.get()}\n"
            f"### Version: {ver_combo.get()}\n"
            f"### Status: {status_combo.get()}\n"
            f"### Details: {error_text.get(1.0, tk.END)}"
        )

        url = f"https://github.com/bestrigyn/shadPS4-Community-Compatibility/issues/new?title={urllib.parse.quote(title)}&body={urllib.parse.quote(body)}"
        open_url(url)
        reg_window.destroy()

    tk.Button(main_frame, text="GENERATE & SEND", command=generate_and_send, bg="#007acc", fg="white",
              font=("Arial", 11, "bold"), height=2).pack(pady=20, fill=tk.X)


# --- ИНТЕРФЕЙС ГЛАВНОГО ОКНА ---
def load_data():
    listbox.delete(0, tk.END)
    url = "https://api.github.com/repos/bestrigyn/shadPS4-Community-Compatibility/issues"
    try:
        with urllib.request.urlopen(url) as res:
            data = json.loads(res.read().decode())
            for issue in data:
                issues_data.append(issue)
                listbox.insert(tk.END, issue['title'])
    except:
        pass


tk.Label(root, text="🎮 shadPS4 DATABASE", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white").pack(pady=15)
listbox = tk.Listbox(root, width=80, height=10, bg="#252526", fg="#cccccc")
listbox.pack(pady=5, padx=20)

tk.Button(root, text="➕ CREATE NEW REPORT", command=open_registration_window, bg="#007acc", fg="white", height=2).pack(
    pady=10, padx=20, fill=tk.X)

load_data()
root.mainloop()
