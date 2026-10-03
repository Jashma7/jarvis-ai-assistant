
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import math

# ---------------- CONFIGURATION ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_FILE = os.path.join(BASE_DIR, "main.py")

BG = "#07111F"
SIDEBAR = "#0A1728"
PANEL = "#101F33"
PANEL_LIGHT = "#152941"
CYAN = "#00D9FF"
BLUE = "#168BFF"
GREEN = "#20E6A2"
RED = "#FF5573"
WHITE = "#EAF5FF"
MUTED = "#8299B5"
BORDER = "#1D3550"

jarvis_process = None
animation_phase = 0
is_running = False

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("JARVIS | AI Assistant")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg=BG)


def rounded_button(parent, text, command, bg, fg=WHITE):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=bg,
        fg=fg,
        activebackground=CYAN,
        activeforeground=BG,
        relief="flat",
        bd=0,
        padx=20,
        pady=13,
        cursor="hand2"
    )


# ---------------- PROCESS CONTROL ----------------

def start_jarvis():
    global jarvis_process, is_running

    if jarvis_process is not None and jarvis_process.poll() is None:
        status_label.config(text="●  SYSTEM ALREADY ACTIVE", fg=GREEN)
        return

    try:
        jarvis_process = subprocess.Popen(
            [sys.executable, MAIN_FILE],
            cwd=BASE_DIR,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )

        is_running = True
        status_label.config(text="●  JARVIS ONLINE", fg=GREEN)
        model_status.config(text="ACTIVE", fg=GREEN)
        start_button.config(state="disabled", bg="#174D58")
        stop_button.config(state="normal", bg="#742B40")

    except Exception as error:
        messagebox.showerror("JARVIS Error", str(error))


def stop_jarvis():
    global jarvis_process, is_running

    if jarvis_process is not None and jarvis_process.poll() is None:
        jarvis_process.terminate()
        try:
            jarvis_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            jarvis_process.kill()

    jarvis_process = None
    is_running = False
    status_label.config(text="●  SYSTEM STANDBY", fg=RED)
    model_status.config(text="STANDBY", fg=MUTED)
    start_button.config(state="normal", bg="#087B9B")
    stop_button.config(state="disabled", bg="#3B2937")


def close_app():
    stop_jarvis()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)


# ---------------- SIDEBAR ----------------

sidebar = tk.Frame(root, bg=SIDEBAR, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

brand = tk.Frame(sidebar, bg=SIDEBAR)
brand.pack(fill="x", padx=22, pady=(27, 35))

tk.Label(
    brand,
    text="◈",
    font=("Segoe UI Symbol", 30, "bold"),
    fg=CYAN,
    bg=SIDEBAR
).pack(side="left")

tk.Label(
    brand,
    text="JARVIS",
    font=("Segoe UI", 19, "bold"),
    fg=WHITE,
    bg=SIDEBAR
).pack(side="left", padx=9)

tk.Label(
    sidebar,
    text="MAIN MENU",
    font=("Segoe UI", 9, "bold"),
    fg="#59738F",
    bg=SIDEBAR
).pack(anchor="w", padx=24, pady=(0, 12))


def sidebar_item(symbol, label, active=False):
    color = CYAN if active else MUTED
    background = "#112940" if active else SIDEBAR

    item = tk.Frame(sidebar, bg=background, height=45)
    item.pack(fill="x", padx=12, pady=3)
    item.pack_propagate(False)

    tk.Label(
        item,
        text=symbol,
        font=("Segoe UI", 14),
        fg=color,
        bg=background,
        width=3
    ).pack(side="left", padx=(7, 2))

    tk.Label(
        item,
        text=label,
        font=("Segoe UI", 10, "bold" if active else "normal"),
        fg=WHITE if active else MUTED,
        bg=background
    ).pack(side="left")


sidebar_item("⌂", "Dashboard", True)
sidebar_item("◉", "Voice Assistant")
sidebar_item("✧", "AI Intelligence")
sidebar_item("◷", "Activity")
sidebar_item("⚙", "Settings")

tk.Frame(sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

sidebar_bottom = tk.Frame(sidebar, bg=SIDEBAR)
sidebar_bottom.pack(fill="x", padx=20, pady=22)

tk.Frame(sidebar_bottom, bg=BORDER, height=1).pack(fill="x", pady=(0, 15))

tk.Label(
    sidebar_bottom,
    text="LOCAL AI ENGINE",
    font=("Segoe UI", 8, "bold"),
    fg="#59738F",
    bg=SIDEBAR
).pack(anchor="w")

tk.Label(
    sidebar_bottom,
    text="●  Ollama  •  Llama 3.2",
    font=("Segoe UI", 9),
    fg=GREEN,
    bg=SIDEBAR
).pack(anchor="w", pady=7)


# ---------------- MAIN CONTENT ----------------

main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

# Top bar
topbar = tk.Frame(main, bg=BG)
topbar.pack(fill="x", padx=32, pady=(24, 12))

heading_frame = tk.Frame(topbar, bg=BG)
heading_frame.pack(side="left")

tk.Label(
    heading_frame,
    text="AI CONTROL CENTER",
    font=("Segoe UI", 17, "bold"),
    fg=WHITE,
    bg=BG
).pack(anchor="w")

tk.Label(
    heading_frame,
    text="Your personal intelligent voice assistant",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG
).pack(anchor="w", pady=(3, 0))

status_label = tk.Label(
    topbar,
    text="●  SYSTEM STANDBY",
    font=("Segoe UI", 9, "bold"),
    fg=RED,
    bg=BG
)
status_label.pack(side="right", padx=4)


# ---------------- AI CORE PANEL ----------------

hero = tk.Frame(
    main,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)
hero.pack(fill="both", expand=True, padx=30, pady=12)

tk.Label(
    hero,
    text="JARVIS NEURAL CORE",
    font=("Segoe UI", 11, "bold"),
    fg=CYAN,
    bg=PANEL
).pack(pady=(20, 2))

tk.Label(
    hero,
    text="Voice interface ready",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=PANEL
).pack()

# Animated core
canvas = tk.Canvas(
    hero,
    width=280,
    height=230,
    bg=PANEL,
    highlightthickness=0
)
canvas.pack(pady=(2, 0))

center_x = 140
center_y = 112


def animate_core():
    global animation_phase

    canvas.delete("core")

    pulse = (math.sin(animation_phase) + 1) / 2
    outer = 83 + pulse * 8
    middle = 65 + pulse * 5
    inner = 44 + pulse * 3

    canvas.create_oval(
        center_x - outer, center_y - outer,
        center_x + outer, center_y + outer,
        outline="#164C6C",
        width=2,
        tags="core"
    )

    canvas.create_oval(
        center_x - middle, center_y - middle,
        center_x + middle, center_y + middle,
        outline="#087EAD",
        width=2,
        tags="core"
    )

    canvas.create_oval(
        center_x - inner, center_y - inner,
        center_x + inner, center_y + inner,
        fill="#0D304B",
        outline=CYAN,
        width=2,
        tags="core"
    )

    canvas.create_text(
        center_x, center_y,
        text="J",
        font=("Segoe UI", 49, "bold"),
        fill=CYAN,
        tags="core"
    )

    # Decorative orbit points
    for i in range(8):
        angle = animation_phase + i * math.pi / 4
        radius = outer + 7
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius

        canvas.create_oval(
            x - 2, y - 2, x + 2, y + 2,
            fill=CYAN,
            outline="",
            tags="core"
        )

    animation_phase += 0.045
    root.after(45, animate_core)


animate_core()

tk.Label(
    hero,
    text="SAY  “HEY JARVIS”  TO ACTIVATE",
    font=("Segoe UI", 10, "bold"),
    fg=WHITE,
    bg=PANEL
).pack(pady=(0, 13))

# Start / Stop controls
controls = tk.Frame(hero, bg=PANEL)
controls.pack(pady=(0, 17))

start_button = rounded_button(
    controls, "▶   START JARVIS", start_jarvis, "#087B9B"
)
start_button.grid(row=0, column=0, padx=7)

stop_button = rounded_button(
    controls, "■   STOP", stop_jarvis, "#3B2937"
)
stop_button.grid(row=0, column=1, padx=7)
stop_button.config(state="disabled")


# ---------------- STATUS CARDS ----------------

cards = tk.Frame(main, bg=BG)
cards.pack(fill="x", padx=30, pady=(3, 10))

def make_card(parent, title, value, accent):
    card = tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 9),
        fg=MUTED,
        bg=PANEL
    ).pack(anchor="w", padx=14, pady=(12, 4))

    value_label = tk.Label(
        card,
        text=value,
        font=("Segoe UI", 11, "bold"),
        fg=accent,
        bg=PANEL
    )
    value_label.pack(anchor="w", padx=14, pady=(0, 13))

    return value_label


model_status = make_card(cards, "AI MODEL", "STANDBY", CYAN)
make_card(cards, "ENGINE", "OLLAMA", GREEN)
make_card(cards, "WAKE WORD", "HEY JAR", WHITE)


# ---------------- FOOTER ----------------

footer = tk.Frame(main, bg=BG)
footer.pack(fill="x", padx=34, pady=(0, 13))

tk.Label(
    footer,
    text="JARVIS AI  •  PYTHON  •  LLAMA 3.2",
    font=("Segoe UI", 8),
    fg="#59738F",
    bg=BG
).pack(side="left")

tk.Label(
    footer,
    text="LOCAL ASSISTANT",
    font=("Segoe UI", 8, "bold"),
    fg=GREEN,
    bg=BG
).pack(side="right")

root.mainloop()

