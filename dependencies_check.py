import subprocess

def check_and_install_dependencies():
    dependencies = {
        "bluez": {"installer": install_via_apt, "type": "tool"},
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
        "hciconfig": {"installer": install_via_apt, "type": "tool", "package": "bluez"},
        "psutil": {"installer": install_via_pip, "type": "python-lib", "package": "psutil"},

    }

    for name, details in dependencies.items():
        if details["type"] == "tool":
            if not is_tool_installed(name):
                print(f"{name} is not installed.")
                choice = input(f"Do you want to install {name} via apt? (yes/no): ")
                if choice.lower() == 'yes':
                    package = details.get("package", name)
                    details["installer"](package)

        elif details["type"] == "pip_package":
            try:
                # Check if the pip package is installed
                subprocess.run(['pip', 'show', name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print(f"{name} is not installed.")
                choice = input(f"Do you want to install {name} via pip? (yes/no): ")
                if choice.lower() == 'yes':
                    details["installer"](name)

def is_tool_installed(tool):
    try:
        subprocess.run([tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return True  # Tool is installed but returned a non-zero exit code
    except FileNotFoundError:
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