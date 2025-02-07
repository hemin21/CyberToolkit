import scapy.all as scapy
import pyshark
import socket
import asyncio
import tkinter as tk
from tkinter import scrolledtext, Button, Label, ttk, StringVar, messagebox, Frame
from collections import defaultdict
from threading import Thread
import psutil

# Dictionary to store connection counts for anomaly detection
connection_logs = defaultdict(int)
THRESHOLD = 20  # Define an anomaly threshold (e.g., 20 requests in 10 sec)
stop_sniffing = False  # Global flag to stop sniffing
selected_adapter = None  # Variable to store user-selected adapter


# Function to get available network adapters
def get_network_adapters():
    return list(psutil.net_if_addrs().keys())


# Function to resolve domain names
def resolve_domain(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return ip


# Function to ask user for mode
def ask_mode():
    mode = input("Choose mode (1 - Terminal, 2 - GUI): ")
    return mode.strip()


# GUI Setup
def setup_gui():
    global log_text, http_text, tcp_text, udp_text, root, adapter_var, adapter_menu, filter_var
    root = tk.Tk()
    root.title("CyberSniffer - Network Monitor")
    root.geometry("1000x600")
    root.configure(bg="white")

    Label(root, text="Select Network Adapter:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)
    adapter_var = StringVar(root)
    adapters = get_network_adapters()
    if adapters:
        adapter_var.set(adapters[0])
    adapter_menu = ttk.Combobox(root, textvariable=adapter_var, values=adapters, state="readonly")
    adapter_menu.pack(pady=5)

    Label(root, text="All Requests:", font=("Arial", 12), bg="white", fg="black").pack()
    log_text = scrolledtext.ScrolledText(root, width=120, height=10, font=("Arial", 10), bg="white", fg="black")
    log_text.pack(pady=5)

    Label(root, text="HTTP/HTTPS/FTP Traffic:", font=("Arial", 12), bg="white", fg="black").pack()
    http_text = scrolledtext.ScrolledText(root, width=120, height=5, font=("Arial", 10), bg="white", fg="black")
    http_text.pack(pady=5)

    Label(root, text="TCP Traffic:", font=("Arial", 12), bg="white", fg="black").pack()
    tcp_text = scrolledtext.ScrolledText(root, width=120, height=5, font=("Arial", 10), bg="white", fg="black")
    tcp_text.pack(pady=5)

    Label(root, text="UDP Traffic:", font=("Arial", 12), bg="white", fg="black").pack()
    udp_text = scrolledtext.ScrolledText(root, width=120, height=5, font=("Arial", 10), bg="white", fg="black")
    udp_text.pack(pady=5)

    button_frame = Frame(root, bg="white")
    button_frame.pack(side=tk.BOTTOM, pady=10)

    start_button = Button(button_frame, text="Start Sniffing", command=start_sniffing, font=("Arial", 10), bg="green",
                          fg="white")
    start_button.pack(side=tk.LEFT, padx=5)

    stop_button = Button(button_frame, text="Stop", command=stop_sniffing_action, font=("Arial", 10), fg="white",
                         bg="red")
    stop_button.pack(side=tk.LEFT, padx=5)

    reset_button = Button(button_frame, text="Reset", command=reset_logs, font=("Arial", 10), fg="white", bg="blue")
    reset_button.pack(side=tk.LEFT, padx=5)

    root.after(1000, update_gui)
    root.mainloop()


# Function to update GUI logs
def update_gui():
    log_text.yview(tk.END)
    http_text.yview(tk.END)
    tcp_text.yview(tk.END)
    udp_text.yview(tk.END)
    log_text.after(1000, update_gui)


# Stop sniffing function
def stop_sniffing_action():
    global stop_sniffing
    stop_sniffing = True


# Reset logs function
def reset_logs():
    log_text.delete('1.0', tk.END)
    http_text.delete('1.0', tk.END)
    tcp_text.delete('1.0', tk.END)
    udp_text.delete('1.0', tk.END)


# Packet Sniffing Function
def packet_callback(packet):
    if stop_sniffing:
        return

    if packet.haslayer(scapy.IP):
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        domain_dst = resolve_domain(ip_dst)
        port = packet[scapy.IP].sport if packet.haslayer(scapy.TCP) or packet.haslayer(scapy.UDP) else "Unknown"
        protocol = "HTTPS" if packet.haslayer(scapy.TCP) and port == 443 else "HTTP" if packet.haslayer(
            scapy.TCP) and port == 80 else "TCP" if packet.haslayer(scapy.TCP) else "UDP"
        log_entry = f"[{protocol}] {ip_src} -> {domain_dst} | Port: {port}\n"
        print(log_entry)
        log_text.insert(tk.END, log_entry)
        connection_logs[ip_src] += 1

        if protocol in ["HTTP", "HTTPS"]:
            http_text.insert(tk.END, log_entry)
        elif protocol == "TCP":
            tcp_text.insert(tk.END, log_entry)
        elif protocol == "UDP":
            udp_text.insert(tk.END, log_entry)


# Start Sniffing
def start_sniffing():
    global stop_sniffing, selected_adapter
    stop_sniffing = False
    selected_adapter = adapter_var.get()
    if not selected_adapter:
        log_text.insert(tk.END, "[ERROR] No network adapter selected!\n")
        return
    print(f"[INFO] Starting CyberSniffer on {selected_adapter}...")

    sniff_thread = Thread(
        target=lambda: scapy.sniff(filter="ip", prn=packet_callback, store=False, iface=selected_adapter), daemon=True)
    sniff_thread.start()


if __name__ == "__main__":
    mode = ask_mode()
    if mode == "1":
        print("[INFO] Running in Terminal mode...")
        adapters = get_network_adapters()
        for idx, adapter in enumerate(adapters):
            print(f"{idx + 1}. {adapter}")
        selected_index = int(input("Enter the number of the network adapter to sniff: ")) - 1
        selected_adapter = adapters[selected_index]
        start_sniffing()
    elif mode == "2":
        setup_gui()
    else:
        print("Invalid option. Exiting...")
