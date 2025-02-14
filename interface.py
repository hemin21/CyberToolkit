import os
import pyfiglet

def display_banner():
    os.system("clear" if os.name == "posix" else "cls")  # Clears screen

    banner_text = pyfiglet.figlet_format("CodeWave Crew", font="slant")
    print(f"\033[92m{banner_text}\033[0m")

    print("[X] Toolkit - Ethical Hacking Suite [X]\n")
    print("⚠ Please use responsibly for security research & educational purposes only.\n")

# ======== TOOL FUNCTIONS ========

def install_cupp():
    print("\nInstalling Cupp...\n")
    os.system("git clone https://github.com/Mebus/cupp.git && chmod +x cupp/cupp.py")
    print("\nInstallation complete!")

def run_cupp():
    if os.path.exists("cupp/cupp.py"):
        os.system("python3 cupp/cupp.py")
    else:
        print("\nCupp is not installed! Please install it first.")

def install_nmap():
    print("\nInstalling Nmap...\n")
    os.system("sudo apt install nmap -y")
    print("\nInstallation complete!")

def run_nmap():
    os.system("nmap -h")

def install_rdesktop():
    print("\nInstalling rdesktop...\n")
    os.system("sudo apt install rdesktop -y")
    print("\nInstallation complete!")

def run_rdesktop():
    ip = input("Enter target IP: ")
    os.system(f"rdesktop {ip}")

def install_sqlmap():
    print("\nInstalling Sqlmap...\n")
    os.system("git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev")
    print("\nInstallation complete!")

def run_sqlmap():
    os.system("python3 sqlmap-dev/sqlmap.py -h")

def install_aircrack():
    print("\nInstalling Aircrack-ng...\n")
    os.system("sudo apt install aircrack-ng -y")
    print("\nInstallation complete!")

def run_aircrack():
    os.system("airmon-ng")

def install_openvpn():
    print("\nInstalling OpenVPN...\n")
    os.system("sudo apt install openvpn -y")
    print("\nInstallation complete!")

def run_openvpn():
    config = input("Enter OpenVPN config file path: ")
    os.system(f"sudo openvpn {config}")

# ======== SUB-MENUS FOR TOOLS ========

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
        ("Cupp (Wordlist Maker)", install_cupp, run_cupp),
        ("Nmap (Network Scanner)", install_nmap, run_nmap),
        ("RDP (Remote Desktop Protocol)", install_rdesktop, run_rdesktop),
        ("Sqlmap (SQL Injection)", install_sqlmap, run_sqlmap),
        ("Aircrack-ng (WiFi Hacking)", install_aircrack, run_aircrack),
        ("OpenVPN (VPN Connection)", install_openvpn, run_openvpn),
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
