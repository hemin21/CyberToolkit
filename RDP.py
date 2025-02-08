import subprocess

def remote_rdp(server_ip, username, password):
    try:
        print(f"Starting RDP session to {server_ip}...")
        command = ["xfreerdp", f"/u:{username}", f"/p:{password}", f"/v:{server_ip}", "/dynamic-resolution"]
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    server_ip = input("Enter remote server IP: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    remote_rdp(server_ip, username, password)
