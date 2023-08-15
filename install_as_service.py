import os
import subprocess

SERVICE_NAME = "run_diagnostics_after_desktop.service"
SERVICE_PATH = f"/etc/systemd/system/{SERVICE_NAME}"
SCRIPT_PATH = "/usr/local/bin/run_in_terminal.sh"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT_PATH = os.path.join(CURRENT_DIR, "diagnostics.py")


def create_service_script():
    with open(SCRIPT_PATH, 'w') as f:
        f.write("#!/bin/bash\n\n")
        f.write("sleep 10\n")  # Wait for 10 seconds to ensure X server is ready.
        f.write(f"lxterminal -e \"bash -c 'sudo python {MAIN_SCRIPT_PATH}; bash'\"")

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
