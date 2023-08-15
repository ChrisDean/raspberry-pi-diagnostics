import os
import subprocess

SERVICE_NAME = "run_diagnostics_after_desktop.service"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"
SCRIPT_PATH = "/usr/local/bin/run_in_terminal.sh"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT_PATH = os.path.join(CURRENT_DIR, "diagnostics.py")


def create_service_script():
    with open(SCRIPT_PATH, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("exec > /tmp/diagnostics.log 2>&1\n")  # Redirect stdout and stderr to a log file.
        f.write("set -x\n")  # Enable bash debugging.

        f.write("export NO_AT_BRIDGE=1\n")  # prevent issues with accessing the accessibility bus

        f.write("sleep 20\n")  # Wait for 10 seconds to ensure X server is ready.
        # Open lxterminal without waiting for it to close.
        f.write(f"lxterminal -e \"bash -c 'sudo python {MAIN_SCRIPT_PATH}; bash'\" &\n")
        # Wait a bit to ensure the terminal has opened.
        f.write("sleep 2\n")
        # Use wmctrl to set the lxterminal to fullscreen.
        f.write("wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz\n")

    os.chmod(SCRIPT_PATH, 0o755)


def create_service():
    service_content = f"""[Unit]
Description=Run diagnostics script in terminal after desktop loads
After=graphical.target

[Service]
User=pi
Group=pi
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart={SCRIPT_PATH}

[Install]
WantedBy=graphical.target
"""

    with open(SERVICE_PATH, 'w') as f:
        f.write(service_content)

    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "enable", SERVICE_NAME])


def remove_service():
    if os.path.exists(SERVICE_PATH):
        subprocess.run(["sudo", "systemctl", "disable", SERVICE_NAME])
        os.remove(SERVICE_PATH)

    if os.path.exists(SCRIPT_PATH):
        os.remove(SCRIPT_PATH)

    subprocess.run(["sudo", "systemctl", "daemon-reload"])


def main():
    choice = input("Do you want to setup (s) or remove (r) the service? [s/r]: ").strip().lower()

    if choice == 's':
        create_service_script()
        create_service()
        print(f"Service {SERVICE_NAME} has been set up!")
    elif choice == 'r':
        remove_service()
        print(f"Service {SERVICE_NAME} has been removed!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()
