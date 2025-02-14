import os
import subprocess
import pyfiglet

# Path where tools are stored
TOOLS_DIR = "Tool/"


def display_banner():
    os.system("clear" if os.name == "posix" else "cls")
    banner_text = pyfiglet.figlet_format("CodeWave Crew", font="slant")
    print(f"\033[92m{banner_text}\033[0m")
    print("[X] Toolkit - Ethical Hacking Suite [X]\n")
    print("⚠ Please use responsibly for security research & educational purposes only.\n")


# Function to get all tools from the Tool folder
def get_available_tools():
    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR)  # Ensure the folder exists
    return [f for f in os.listdir(TOOLS_DIR) if os.path.isfile(os.path.join(TOOLS_DIR, f))]


# Function to install tools
def install_tool(tool_name):
    tool_path = os.path.join(TOOLS_DIR, tool_name)

    if tool_name.endswith(".py"):
        install_command = f"python {tool_path} --install"
    elif tool_name.endswith(".sh"):
        install_command = f"bash {tool_path} --install"
    else:
        print(f"Unsupported tool format: {tool_name}")
        return

    open_terminal(install_command)


# Function to run tools
def run_tool(tool_name):
    tool_path = os.path.join(TOOLS_DIR, tool_name)

    if tool_name.endswith(".py"):
        run_command = f"python {tool_path}"
    elif tool_name.endswith(".sh"):
        run_command = f"bash {tool_path}"
    else:
        print(f"Unsupported tool format: {tool_name}")
        return

    open_terminal(run_command)


# Function to open a new terminal and execute a command
def open_terminal(command):
    if os.name == "posix":  # Linux/macOS
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"], shell=False)
    else:  # Windows
        subprocess.Popen(f'start cmd /k {command}', shell=True)


# Main menu function
def main_menu():
    while True:
        display_banner()
        tools = get_available_tools()

        if not tools:
            print("No tools found in the 'Tool' folder. Please add some!")
            break

        # Display available tools
        for i, tool in enumerate(tools, start=1):
            print(f"[{i}] {tool}")

        print(f"[{len(tools) + 1}] Exit")

        try:
            choice = int(input("\nChoose a tool to proceed: "))
            if 1 <= choice <= len(tools):
                tool_name = tools[choice - 1]
                tool_options(tool_name)
            elif choice == len(tools) + 1:  # Exit option
                print("Exiting Toolkit...")
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input! Please enter a number.")


# Tool menu for Install/Run
def tool_options(tool_name):
    while True:
        print(f"\n[{tool_name}]\n[1] Install {tool_name}\n[2] Run {tool_name}\n[3] Back to Main Menu")
        try:
            choice = int(input("\nChoose an option: "))
            if choice == 1:
                install_tool(tool_name)
            elif choice == 2:
                run_tool(tool_name)
            elif choice == 3:
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input! Please enter a number.")


# Start the script
if __name__ == "__main__":
    main_menu()
