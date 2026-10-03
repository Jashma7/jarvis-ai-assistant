
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import queue
import json
import sys
from pathlib import Path
from datetime import datetime

# -------------------- FILES --------------------

BASE_DIR = Path(__file__).resolve().parent
MAIN_FILE = BASE_DIR / "main.py"
HISTORY_FILE = BASE_DIR / "chat_history.json"
SETTINGS_FILE = BASE_DIR / "jarvis_settings.json"

# -------------------- DEFAULT SETTINGS --------------------

DEFAULT_SETTINGS = {
    "assistant_name": "Jarvis",
    "voice_speed": 1.0,
    "theme": "Dark"
}

def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                saved = json.load(file)
            settings = DEFAULT_SETTINGS.copy()
            if isinstance(saved, dict):
                settings.update(saved)
            return settings
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_SETTINGS.copy()

settings = load_settings()

def save_settings():
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)
    except OSError as error:
        messagebox.showerror("Settings Error", str(error))

# -------------------- THEMES --------------------

THEMES = {
    "Dark": {
        "bg": "#0b1020",
        "panel": "#111a2e",
        "card": "#17233b",
        "chat": "#0d1628",
        "text": "#eaf2ff",
        "muted": "#91a4c7",
        "accent": "#00d4ff",
        "green": "#22c55e",
        "red": "#ef4444"
    },
    "Light": {
        "bg": "#edf2f8",
        "panel": "#ffffff",
        "card": "#e1eaf5",
        "chat": "#f7faff",
        "text": "#172033",
        "muted": "#596b85",
        "accent": "#0077cc",
        "green": "#15803d",
        "red": "#dc2626"
    }
}

theme = THEMES.get(settings["theme"], THEMES["Dark"])

BG = theme["bg"]
PANEL = theme["panel"]
CARD = theme["card"]
CHAT_BG = theme["chat"]
TEXT = theme["text"]
MUTED = theme["muted"]
ACCENT = theme["accent"]
GREEN = theme["green"]
RED = theme["red"]

# -------------------- CHAT HISTORY --------------------

def load_chat_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []

chat_history = load_chat_history()

def save_chat_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(chat_history, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print("Could not save chat history:", error)

# -------------------- MAIN WINDOW --------------------

root = tk.Tk()
root.title("JARVIS AI Assistant")
root.geometry("1100x700")
root.minsize(850, 550)
root.configure(bg=BG)

events = queue.Queue()
process = None
running = False
core_phase = 0

# -------------------- HEADER --------------------

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=22, pady=(18, 10))

title_label = tk.Label(
    header,
    text="J.A.R.V.I.S",
    font=("Segoe UI", 24, "bold"),
    fg=ACCENT,
    bg=BG
)
title_label.pack(side="left")

subtitle = tk.Label(
    header,
    text="PERSONAL AI VOICE ASSISTANT",
    font=("Segoe UI", 9, "bold"),
    fg=MUTED,
    bg=BG
)
subtitle.pack(side="left", padx=16, pady=(10, 0))

# -------------------- LAYOUT --------------------

content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=22, pady=10)

sidebar = tk.Frame(content, bg=PANEL, width=190)
sidebar.pack(side="left", fill="y", padx=(0, 14))
sidebar.pack_propagate(False)

main_area = tk.Frame(content, bg=BG)
main_area.pack(side="left", fill="both", expand=True)

# -------------------- SIDEBAR --------------------

side_heading = tk.Label(
    sidebar,
    text="CONTROL PANEL",
    font=("Segoe UI", 10, "bold"),
    fg=MUTED,
    bg=PANEL
)
side_heading.pack(anchor="w", padx=16, pady=(22, 18))

status_label = tk.Label(
    sidebar,
    text="● OFFLINE",
    font=("Segoe UI", 11, "bold"),
    fg=RED,
    bg=PANEL
)
status_label.pack(anchor="w", padx=16, pady=(0, 20))

def make_button(parent, text, command, color=None):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        fg=color or ACCENT,
        bg=CARD,
        activeforeground=TEXT,
        activebackground=theme["panel"],
        relief="flat",
        bd=0,
        padx=10,
        pady=12,
        cursor="hand2"
    )

# -------------------- CHAT PANEL --------------------

chat_card = tk.Frame(main_area, bg=PANEL)
chat_card.pack(side="left", fill="both", expand=True, padx=(0, 14))

chat_header = tk.Frame(chat_card, bg=PANEL)
chat_header.pack(fill="x", padx=18, pady=(16, 10))

chat_title = tk.Label(
    chat_header,
    text="LIVE CONVERSATION",
    font=("Segoe UI", 12, "bold"),
    fg=TEXT,
    bg=PANEL
)
chat_title.pack(side="left")

# -------------------- CHAT DISPLAY --------------------

chat_display = scrolledtext.ScrolledText(
    chat_card,
    wrap=tk.WORD,
    font=("Segoe UI", 10),
    bg=CHAT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    bd=0,
    padx=14,
    pady=14,
    state="disabled"
)
chat_display.pack(fill="both", expand=True, padx=14, pady=(0, 14))

chat_display.tag_config("user", foreground=ACCENT, font=("Segoe UI", 10, "bold"))
chat_display.tag_config("assistant", foreground=GREEN, font=("Segoe UI", 10, "bold"))
chat_display.tag_config("system", foreground=MUTED, font=("Segoe UI", 9, "italic"))

def add_chat_message(kind, message, timestamp=None, save=True):
    timestamp = timestamp or datetime.now().strftime("%H:%M:%S")
    label = {
        "user": "YOU",
        "assistant": settings["assistant_name"].upper(),
        "system": "SYSTEM"
    }.get(kind, "SYSTEM")

    tag = kind if kind in ("user", "assistant", "system") else "system"

    chat_display.configure(state="normal")
    chat_display.insert(tk.END, f"[{timestamp}] {label}\n", tag)
    chat_display.insert(tk.END, f"{message}\n\n")
    chat_display.see(tk.END)
    chat_display.configure(state="disabled")

    if save:
        chat_history.append({
            "type": kind,
            "message": message,
            "time": timestamp
        })
        save_chat_history()

def show_saved_history():
    for item in chat_history:
        if isinstance(item, dict):
            add_chat_message(
                item.get("type", "system"),
                str(item.get("message", "")),
                item.get("time"),
                save=False
            )

def clear_history():
    if not messagebox.askyesno("Clear History", "Delete all saved conversations?"):
        return

    chat_history.clear()
    save_chat_history()
    chat_display.configure(state="normal")
    chat_display.delete("1.0", tk.END)
    chat_display.configure(state="disabled")
    add_chat_message("system", "Chat history cleared.")

clear_button = tk.Button(
    chat_header,
    text="Clear History",
    command=clear_history,
    font=("Segoe UI", 9, "bold"),
    fg=ACCENT,
    bg=CARD,
    activebackground=theme["panel"],
    activeforeground=TEXT,
    relief="flat",
    padx=10,
    pady=6,
    cursor="hand2"
)
clear_button.pack(side="right")

# -------------------- ASSISTANT CORE --------------------

core_card = tk.Frame(main_area, bg=PANEL, width=230)
core_card.pack(side="right", fill="y")
core_card.pack_propagate(False)

core_title = tk.Label(
    core_card,
    text="ASSISTANT CORE",
    font=("Segoe UI", 11, "bold"),
    fg=TEXT,
    bg=PANEL
)
core_title.pack(pady=(20, 12))

core_canvas = tk.Canvas(
    core_card,
    width=190,
    height=220,
    bg=PANEL,
    highlightthickness=0
)
core_canvas.pack(pady=5)

core_circle = core_canvas.create_oval(
    35, 35, 155, 155,
    outline=ACCENT,
    width=3
)
core_inner = core_canvas.create_oval(
    52, 52, 138, 138,
    outline="#2563eb",
    width=2
)
core_text = core_canvas.create_text(
    95, 95,
    text=settings["assistant_name"][:1].upper(),
    fill=ACCENT,
    font=("Segoe UI", 42, "bold")
)

def animate_core():
    global core_phase
    core_phase = (core_phase + 1) % 20
    color = ACCENT if running and core_phase < 10 else (
        "#2563eb" if running else "#40506b"
    )
    core_canvas.itemconfigure(core_circle, outline=color)
    core_canvas.itemconfigure(core_text, fill=color)
    root.after(180, animate_core)

core_status = tk.Label(
    core_card,
    text="SYSTEM OFFLINE",
    font=("Segoe UI", 10, "bold"),
    fg=MUTED,
    bg=PANEL
)
core_status.pack(pady=(8, 18))

# -------------------- STATUS --------------------

def set_status(status):
    status = status.upper()
    colors = {
        "ONLINE": GREEN,
        "LISTENING": ACCENT,
        "THINKING": "#fbbf24",
        "STANDBY": MUTED,
        "OFFLINE": RED
    }
    color = colors.get(status, MUTED)
    status_label.configure(text=f"● {status}", fg=color)
    core_status.configure(text=f"SYSTEM {status}", fg=color)

# -------------------- PROCESS CONTROL --------------------

def read_process_output(proc):
    try:
        for line in iter(proc.stdout.readline, ""):
            line = line.strip()
            if line:
                events.put(line)
    except (OSError, ValueError):
        pass
    finally:
        events.put("__PROCESS_ENDED__")

def start_jarvis():
    global process, running

    if running:
        return

    if not MAIN_FILE.exists():
        add_chat_message("system", "main.py was not found in the project folder.")
        return

    try:
        process = subprocess.Popen(
            [sys.executable, str(MAIN_FILE)],
            cwd=str(BASE_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        running = True
        set_status("ONLINE")
        add_chat_message(
            "system",
            f"{settings['assistant_name']} started. Say Hey Jarvis to activate."
        )

        threading.Thread(
            target=read_process_output,
            args=(process,),
            daemon=True
        ).start()

    except Exception as error:
        running = False
        set_status("OFFLINE")
        add_chat_message("system", f"Could not start assistant: {error}")

def stop_jarvis():
    global process, running

    if process and process.poll() is None:
        process.terminate()
        add_chat_message("system", "Stop requested.")

    running = False
    set_status("OFFLINE")

def process_events():
    global running

    try:
        while True:
            line = events.get_nowait()

            if line == "__PROCESS_ENDED__":
                running = False
                set_status("OFFLINE")
                continue

            if line.startswith("JARVIS_EVENT|"):
                parts = line.split("|", 2)
                if len(parts) == 3:
                    event_type, message = parts[1], parts[2]
                    if event_type == "status":
                        set_status(message)
                    elif event_type in ("user", "assistant"):
                        add_chat_message(event_type, message)
    except queue.Empty:
        pass

    root.after(150, process_events)

# -------------------- SETTINGS WINDOW --------------------

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Jarvis Settings")
    settings_window.geometry("420x430")
    settings_window.resizable(False, False)
    settings_window.configure(bg=PANEL)
    settings_window.transient(root)
    settings_window.grab_set()

    heading = tk.Label(
        settings_window,
        text="⚙  ASSISTANT SETTINGS",
        font=("Segoe UI", 16, "bold"),
        fg=ACCENT,
        bg=PANEL
    )
    heading.pack(pady=(22, 18))

    form = tk.Frame(settings_window, bg=PANEL)
    form.pack(fill="both", expand=True, padx=28)

    tk.Label(
        form,
        text="Assistant name",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT,
        bg=PANEL
    ).pack(anchor="w")

    name_var = tk.StringVar(value=settings["assistant_name"])
    name_entry = tk.Entry(
        form,
        textvariable=name_var,
        font=("Segoe UI", 11),
        bg=CHAT_BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )
    name_entry.pack(fill="x", pady=(6, 16), ipady=8)

    tk.Label(
        form,
        text="Voice speed (1.0 = normal)",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT,
        bg=PANEL
    ).pack(anchor="w")

    speed_var = tk.DoubleVar(value=float(settings["voice_speed"]))
    speed_scale = tk.Scale(
        form,
        from_=0.7,
        to=1.5,
        resolution=0.1,
        orient="horizontal",
        variable=speed_var,
        bg=PANEL,
        fg=TEXT,
        troughcolor=CARD,
        highlightthickness=0,
        activebackground=ACCENT
    )
    speed_scale.pack(fill="x", pady=(2, 14))

    tk.Label(
        form,
        text="Dashboard theme",
        font=("Segoe UI", 10, "bold"),
        fg=TEXT,
        bg=PANEL
    ).pack(anchor="w")

    theme_var = tk.StringVar(value=settings["theme"])
    theme_menu = tk.OptionMenu(form, theme_var, "Dark", "Light")
    theme_menu.configure(
        font=("Segoe UI", 10),
        bg=CARD,
        fg=TEXT,
        activebackground=ACCENT,
        activeforeground=TEXT,
        relief="flat",
        highlightthickness=0
    )
    theme_menu["menu"].configure(
        bg=CARD,
        fg=TEXT,
        activebackground=ACCENT
    )
    theme_menu.pack(fill="x", pady=(6, 18))

    def save_and_close():
        new_name = name_var.get().strip()
        if not new_name:
            messagebox.showwarning(
                "Missing name",
                "Please enter an assistant name.",
                parent=settings_window
            )
            return

        settings["assistant_name"] = new_name
        settings["voice_speed"] = round(float(speed_var.get()), 1)
        settings["theme"] = theme_var.get()
        save_settings()

        messagebox.showinfo(
            "Settings Saved",
            "Settings saved. Close and reopen the dashboard to apply the theme.",
            parent=settings_window
        )
        settings_window.destroy()

    save_button = tk.Button(
        form,
        text="SAVE SETTINGS",
        command=save_and_close,
        font=("Segoe UI", 10, "bold"),
        fg="#07111f",
        bg=ACCENT,
        activebackground="#42e3ff",
        relief="flat",
        cursor="hand2",
        pady=11
    )
    save_button.pack(fill="x", pady=(2, 10))

# -------------------- SIDEBAR BUTTONS --------------------

start_button = make_button(sidebar, "▶  Start Jarvis", start_jarvis, GREEN)
start_button.pack(fill="x", padx=12, pady=5)

stop_button = make_button(sidebar, "■  Stop Jarvis", stop_jarvis, RED)
stop_button.pack(fill="x", padx=12, pady=5)

history_button = make_button(
    sidebar,
    "▤  Chat History",
    lambda: add_chat_message(
        "system",
        "Saved conversations are displayed in the chat panel."
    )
)
history_button.pack(fill="x", padx=12, pady=5)

settings_button = make_button(
    sidebar,
    "⚙  Settings",
    open_settings,
    ACCENT
)
settings_button.pack(fill="x", padx=12, pady=5)

sidebar_note = tk.Label(
    sidebar,
    text="Voice assistant\nPowered by local AI",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=PANEL,
    justify="left"
)
sidebar_note.pack(side="bottom", anchor="w", padx=16, pady=20)

# -------------------- FOOTER --------------------

footer = tk.Label(
    root,
    text="JARVIS AI  •  Local voice assistant  •  Chat history saved on this PC",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG
)
footer.pack(fill="x", padx=22, pady=(0, 12))

# -------------------- STARTUP --------------------

show_saved_history()
process_events()
animate_core()

def on_close():
    global running
    if process and process.poll() is None:
        process.terminate()
    running = False
    save_chat_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
