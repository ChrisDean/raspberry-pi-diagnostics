import subprocess

def check_and_install_dependencies():
    dependencies = {
         "hciconfig": {"installer": install_via_apt, "type": "tool", "package": "bluez"},
        "iwconfig": {"installer": install_via_apt, "type": "tool", "package": "wireless-tools"},
        "hcitool": {"installer": install_via_apt, "type": "tool"},
        "speedtest": {"installer": install_via_apt, "type": "tool", "package": "speedtest-cli"},
        "RPi.GPIO": {"installer": install_via_pip, "type": "pip_package"},
        "raspistill": {"installer": install_via_apt, "type": "tool", "package": "libraspberrypi-bin"},
        "pygame": {"installer": install_via_pip, "type": "pip_package"},
        "amixer": {"installer": install_via_apt, "type": "tool", "package": "alsa-utils"},
        "aplay": {"installer": install_via_apt, "type": "tool", "package": "alsa-utils"},
        "vcgencmd": {"installer": install_via_apt, "type": "tool", "package": "libraspberrypi-bin"},
        "netstat": {"installer": install_via_apt, "type": "tool", "package": "net-tools"},
        "psutil": {"installer": install_via_pip, "type": "python-lib", "package": "psutil"},

    }

    for name, details in dependencies.items():
        if details["type"] == "tool":
            if not is_tool_installed(name):
                print(f"{name} is not installed.")
                choice = input(f"Do you want to install {name} via apt? (yes/no): ").lower()
                if choice in ['yes', 'y']:
                    package = details.get("package", name)
                    details["installer"](package)
                elif choice not in ['no', 'n']:
                    print(f"Invalid choice for {name}. Skipping...")

        elif details["type"] == "pip_package":
            try:
                # Check if the pip package is installed
                subprocess.run(['pip', 'show', name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print(f"{name} is not installed.")
                choice = input(f"Do you want to install {name} via pip? (yes/no): ").lower()
                if choice in ['yes', 'y']:
                    details["installer"](name)
                elif choice not in ['no', 'n']:
                    print(f"Invalid choice for {name}. Skipping...")

def is_tool_installed(tool):
    try:
        subprocess.run(["which", tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False  # Tool is not installed

def prompt_installation(tool):
    answer = input(f"Do you want to install {tool}? [Y/n]: ")
    return answer.lower() in ["y", "yes", ""]


def install_via_apt(package):
    print(f"Installing {package} via apt...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", package], check=True)
        print(f"{package} installed successfully!")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}.")


def install_via_pip(package):
    print(f"Installing {package} via pip...")
    try:
        subprocess.run(["pip", "install", package], check=True)
        print(f"{package} installed successfully!")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}.")

if __name__ == "__main__":
    check_and_install_dependencies()