import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os
from threading import Thread

# Run tools asynchronously
def run_tool(tool_name):
    log_text.insert(tk.END, f"\n[+] Running {tool_name}...\n")
    log_text.yview(tk.END)

    def execute():
        os.system(f"python3 modules/{tool_name}.py")
        log_text.insert(tk.END, f"[+] {tool_name} completed!\n")
        log_text.yview(tk.END)

    Thread(target=execute).start()

# GUI Initialization
root = tk.Tk()
root.title("CyberSecurity Toolkit")
root.geometry("700x800")
root.configure(bg="#1e1e2e")

# Set Icon
try:
    icon = ImageTk.PhotoImage(Image.open("assets/icon.png"))
    root.iconphoto(False, icon)
except Exception as e:
    print(f"Could not load icon: {e}")

# Background Image
try:
    bg_image = Image.open("assets/background.png")
    bg_image = bg_image.resize((700, 800), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Could not load background: {e}")

# Title Label
label = tk.Label(root, text="CyberSecurity Toolkit", font=("Courier New", 20, "bold"), fg="#00ff00", bg="#1e1e2e")
label.pack(pady=20)

# Buttons with Hover Effects
def on_enter(e):
    e.widget.config(bg="#00ff00", fg="black")

def on_leave(e):
    e.widget.config(bg="#2e2e3e", fg="white")

tools = [
    ("Network Scanner", "network_scanner"),
    ("VPN Connector", "vpn_connector"),
    ("RDP Connector", "rdp_connector"),
    ("WiFi Attack", "wifi_attack"),
    ("Phishing Tool", "phishing"),
    ("Payload Generator", "payload_generator"),
    ("DDoS Attack", "ddos_attack"),
    ("Secure File Sharing", "secure_file_share"),
]

for text, tool in tools:
    button = tk.Button(root, text=text, command=lambda t=tool: run_tool(t), font=("Courier New", 12), width=30, bg="#2e2e3e", fg="white", relief="raised")
    button.pack(pady=5)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# Log Output
log_text = scrolledtext.ScrolledText(root, width=80, height=10, font=("Courier New", 10), bg="#101010", fg="#00ff00")
log_text.pack(pady=10)
log_text.insert(tk.END, "[*] Toolkit Initialized...\n")

# Run GUI
root.mainloop()
