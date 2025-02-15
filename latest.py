import os
import subprocess
import pyfiglet

def display_banner():
    os.system("clear" if os.name == "posix" else "cls")
    banner_text = pyfiglet.figlet_format("CodeWave Crew", font="slant")
    print(f"\033[92m{banner_text}\033[0m")
    print("[X] Toolkit - Ethical Hacking Suite [X]\n")
    print("⚠ Please use responsibly for security research & educational purposes only.\n")

# ======== TOOL FUNCTIONS ========

def install_cybersniffer():
    print("\nInstalling CyberSniffer dependencies...\n")
    os.system("pip install scapy pyshark psutil")
    print("\nInstallation complete!")

def run_cybersniffer():
    os.system("python3 CyberSniffer.py")

def install_filetransfer():
    print("\nInstalling FileTransfer tool...\n")
    os.system("sudo apt install curl wget tar unzip -y")
    print("\nInstallation complete!")

def run_filetransfer():
    os.system("bash FileTransfer.sh")

def install_ddos():
    print("\nInstalling dependencies for DDoS tool...\n")
    os.system("sudo apt install python3 -y")
    print("\nInstallation complete!")

def run_ddos():
    os.system("python3 DDos.py")

def install_rdp():
    print("\nInstalling xfreerdp...\n")
    os.system("sudo apt install freerdp2-x11 -y")
    print("\nInstallation complete!")

def run_rdp():
    ip = input("Enter IP Address: ").strip()
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    command = ["xfreerdp", f"/u:{username}", f"/p:{password}", f"/v:{ip}", "/dynamic-resolution"]
    subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def install_urlinspector():
    print("\nInstalling URL Inspector dependencies...\n")
    os.system("pip install requests")
    print("\nInstallation complete!")

def run_urlinspector():
    os.system("python3 URLInspector.py")

def install_phishingtool():
    print("\nInstalling Phishing Tool dependencies...\n")
    os.system("pip install requests")
    print("\nInstallation complete!")

def run_phishingtool():
    os.system("python3 PhishingTool.py")

def install_securefilesharer():
    print("\nInstalling Secure File Sharer dependencies...\n")
    os.system("pip install requests")
    print("\nInstallation complete!")

def run_securefilesharer():
    os.system("python3 SecureFileSharer.py")

# ======== SUB-MENU FUNCTION ========

def tool_menu(tool_name, install_function, run_function):
    """Generic function for handling tool sub-menus."""
    while True:
        print(f"\n[{tool_name}]\n[1] Install {tool_name}\n[2] Run {tool_name}\n[3] Back to Main Menu")
        try:
            choice = int(input("\nChoose an option: "))
            if choice == 1:
                install_function()
            elif choice == 2:
                run_function()
            elif choice == 3:
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input! Please enter a number.")

# ======== MAIN MENU ========

def main_menu():
    tools = [
        ("CyberSniffer (Network Scanning)", install_cybersniffer, run_cybersniffer),
        ("FileTransfer", install_filetransfer, run_filetransfer),
        ("DDoS Attack Tool", install_ddos, run_ddos),
        ("RDP (Remote Desktop Protocol)", install_rdp, run_rdp),
        ("URL Inspector", install_urlinspector, run_urlinspector),
        ("Phishing Tool", install_phishingtool, run_phishingtool),
        ("Secure File Sharer", install_securefilesharer, run_securefilesharer),
        ("Exit", None, None)
    ]

    while True:
        display_banner()
        for i, (tool, _, _) in enumerate(tools, start=1):
            print(f"[{i}] {tool}")

        try:
            choice = int(input("\nChoose a tool to proceed: "))
            if 1 <= choice < len(tools):
                tool_menu(tools[choice - 1][0], tools[choice - 1][1], tools[choice - 1][2])
            elif choice == len(tools):  # Exit option
                print("Exiting Toolkit...")
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    main_menu()
