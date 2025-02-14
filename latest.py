import os

# Function to install tools
def install_tool(tool_name):
    print(f"\n[+] Installing {tool_name}...\n")
    
    if tool_name == "Cupp":
        os.system("sudo apt install cupp -y")
    elif tool_name == "CyberSniffer":
        os.system("sudo apt install nmap -y")
    elif tool_name == "DDoS":
        os.system("git clone https://github.com/cyweb/hammer.git && cd hammer && chmod +x hammer.py")
    elif tool_name == "FileTransfer":
        os.system("sudo apt install openssh-client -y")
    elif tool_name == "RDP":
        os.system("sudo apt install xfreerdp -y")
    elif tool_name == "Secure File Sharer":
        os.system("sudo apt install python3 -y")
    elif tool_name == "URL Inspector":
        os.system("sudo apt install curl -y")
    elif tool_name == "Password Strength Checker":
        os.system("sudo apt install libpam-pwquality -y")
    elif tool_name == "Phishing Detector":
        os.system("git clone https://github.com/htr-tech/zphisher.git && cd zphisher && chmod +x zphisher.sh")
    else:
        print("\n[!] Installation command not available for this tool.")

# Function to run tools
def run_tool(tool_name):
    print(f"\n[+] Running {tool_name}...\n")

    if tool_name == "Cupp":
        os.system("python3 cupp.py")
    elif tool_name == "CyberSniffer":
        os.system("nmap -h")
    elif tool_name == "DDoS":
        os.system("cd hammer && python3 hammer.py")
    elif tool_name == "FileTransfer":
        os.system("scp -h")
    elif tool_name == "RDP":
        os.system("xfreerdp /h")
    elif tool_name == "Secure File Sharer":
        os.system("python3 secure_fileshare.py")
    elif tool_name == "URL Inspector":
        os.system("curl --help")
    elif tool_name == "Password Strength Checker":
        os.system("pwscore")
    elif tool_name == "Phishing Detector":
        os.system("cd zphisher && bash zphisher.sh")
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
                    break  # Go back to the main menu
                else:
                    print("\n[!] Invalid option. Try again.")
        elif choice == 10:
            print("\n[+] Exiting...\n")
            break
        else:
            print("\n[!] Invalid option. Try again.")
    else:
        print("\n[!] Invalid input. Enter a number.")
