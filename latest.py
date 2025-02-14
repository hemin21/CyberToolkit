import os
import subprocess

# Function to install tools
def install_tool(tool_name):
    print(f"\n[+] Installing {tool_name}...\n")

    commands = {
        "Cupp": "sudo apt update --fix-missing && sudo apt install cupp -y || git clone https://github.com/Mebus/cupp.git",
        "CyberSniffer": "sudo apt install nmap -y",
        "DDoS": "git clone https://github.com/cyweb/hammer.git && cd hammer && chmod +x hammer.py",
        "FileTransfer": "sudo apt install openssh-client -y",
        "RDP": "sudo apt install xfreerdp -y",
        "Secure File Sharer": "sudo apt install python3 -y",
        "URL Inspector": "sudo apt install curl -y",
        "Password Strength Checker": "sudo apt install libpam-pwquality -y",
        "Phishing Detector": "git clone https://github.com/htr-tech/zphisher.git && cd zphisher && chmod +x zphisher.sh"
    }

    command = commands.get(tool_name)
    if command:
        os.system(command)
    else:
        print("\n[!] Installation command not available for this tool.")

# Function to run tools
def run_tool(tool_name):
    print(f"\n[+] Running {tool_name}...\n")

    commands = {
        "Cupp": "python3 ~/cupp/cupp.py || cupp -h",
        "CyberSniffer": "nmap -h",
        "DDoS": "python3 ~/hammer/hammer.py",
        "FileTransfer": "scp --help",
        "RDP": "xfreerdp --help",
        "Secure File Sharer": "python3 secure_fileshare.py",
        "URL Inspector": "curl --help",
        "Password Strength Checker": "pwscore",
        "Phishing Detector": "bash ~/zphisher/zphisher.sh"
    }

    command = commands.get(tool_name)
    if command:
        subprocess.run(command, shell=True)
    else:
        print("\n[!] Run command not available for this tool.")

# Main menu
tools = [
    "Cupp", "CyberSniffer", "DDoS", "FileTransfer", "RDP",
    "Secure File Sharer", "URL Inspector", "Password Strength Checker", "Phishing Detector"
]

while True:
    print("\n[Cybersecurity Toolkit]")
    for i, tool in enumerate(tools, start=1):
        print(f"[{i}] {tool}")
    print("[10] Exit")

    choice = input("\nChoose a tool: ")

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(tools):
            selected_tool = tools[choice - 1]

            while True:
                print(f"\n[{selected_tool}]")
                print("[1] Install")
                print("[2] Run")
                print("[3] Back to Main Menu")

                option = input("\nChoose an option: ")

                if option == "1":
                    install_tool(selected_tool)
                elif option == "2":
                    run_tool(selected_tool)
                elif option == "3":
                    break
                else:
                    print("\n[!] Invalid option. Try again.")
        elif choice == 10:
            print("\n[+] Exiting...\n")
            break
        else:
            print("\n[!] Invalid option. Try again.")
    else:
        print("\n[!] Invalid input. Enter a number.")
