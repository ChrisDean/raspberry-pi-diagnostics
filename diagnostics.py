import os
import subprocess
import json
import RPi.GPIO as GPIO
import pygame
import datetime
import psutil

def master_test():
    results = {}  # Central JSON object to collect the outputs of each test

    tests = [
        ("Raspberry Pi Version", raspberry_pi_version),
        ("Memory Info", memory_info),
        ("CPU Info", cpu_info),
        ("SD Card Performance", sd_card_performance),
        ("Ethernet Port Status", ethernet_port_status),
        ("Ethernet Speed", ethernet_speed),
        ("Wifi Adapter Status", wifi_adapter_status),
        ("Wifi Availability", wifi_availability),
        ("Bluetooth Availability", bluetooth_availability),
        ("USB Ports", usb_ports),
        ("USB Ports Test", usb_ports_test),
        ("GPIO Pins", gpio_pins),
        ("GPIO Pins Test", gpio_pins_test),
        ("Camera Port Test", camera_port_test),
        ("Display Port", display_port_test),
        ("HDMI Port", hdmi_port_test),
        ("Audio Jack", audio_jack_test),
        ("CPU Temperature", get_cpu_temperature),
        ("Voltages", get_voltages),
        ("CPU Utilization", get_cpu_utilization),
        ("GPU Memory", get_gpu_memory),
        ("Clock Frequencies", get_clock_frequencies),
        ("Disk I/O", get_disk_io),
        ("Hardware Codecs", get_hardware_codecs),
        ("IRQ (Interrupts) Statistics", get_irq_statistics),
        ("Network Statistics", get_network_stats),
        ("Bluetooth Info", get_bluetooth_info),
        ("Storage Space", get_storage_space),
        ("Uptime", get_uptime),
    ]

    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        result = test_func()
        results[test_name] = result
        print(f"Outcome for {test_name}: {result}")
        print("=" * 40)

    return results


def raspberry_pi_version():
    # Create a dictionary of known Raspberry Pi revision codes and their descriptions
    revisions = {
        "0002": "Raspberry Pi Model B Rev 1",
        "0003": "Raspberry Pi Model B Rev 1 ECN0001 (no fuses, D14 removed)",
        "0004": "Raspberry Pi Model B Rev 2",
        "0005": "Raspberry Pi Model B Rev 2",
        "0006": "Raspberry Pi Model B Rev 2",
        "0007": "Raspberry Pi Model A",
        "0008": "Raspberry Pi Model A",
        "0009": "Raspberry Pi Model A",
        "000d": "Raspberry Pi Model B Rev 2",
        "000e": "Raspberry Pi Model B Rev 2",
        "000f": "Raspberry Pi Model B Rev 2",
        "0010": "Raspberry Pi Model B+ Rev 1.2",
        "0011": "Raspberry Pi Compute Module 1",
        "0012": "Raspberry Pi Model A+ Rev 1.1",
        "0013": "Raspberry Pi Model B+ Rev 1.2",
        "0014": "Raspberry Pi Compute Module 1",
        "0015": "Raspberry Pi Model A+ Rev 1.1",
        "a01040": "Raspberry Pi 2 Model B Rev 1.0",
        "a01041": "Raspberry Pi 2 Model B Rev 1.1",
        "a21041": "Raspberry Pi 2 Model B Rev 1.1",
        "a22042": "Raspberry Pi 2 Model B Rev 1.2",
        "900021": "Raspberry Pi Model A+ Rev 1.1",
        "900032": "Raspberry Pi Model B+ Rev 1.2",
        "900092": "Raspberry Pi Zero Rev 1.2",
        "900093": "Raspberry Pi Zero Rev 1.3",
        "9000c1": "Raspberry Pi Zero W",
        "9020e0": "Raspberry Pi 3 Model A+",
        "a02082": "Raspberry Pi 3 Model B Rev 1.2",
        "a020a0": "Raspberry Pi Compute Module 3 Rev 1.0",
        "a020d3": "Raspberry Pi 3 Model B+",
        "a22082": "Raspberry Pi 3 Model B Rev 1.2",
        "a220a0": "Raspberry Pi Compute Module 3 Rev 1.0",
        "a32082": "Raspberry Pi 3 Model B Rev 1.2",
        "a52082": "Raspberry Pi 3 Model B Rev 1.2",
        "a22083": "Raspberry Pi 3 Model B Rev 1.3",
        "a02100": "Raspberry Pi Compute Module 3+ Rev 1.0",
        "a03111": "Raspberry Pi 4 Model B Rev 1.1 (1GB RAM)",
        "b03111": "Raspberry Pi 4 Model B Rev 1.1 (2GB RAM)",
        "c03111": "Raspberry Pi 4 Model B Rev 1.1 (4GB RAM)",
        "c03112": "Raspberry Pi 4 Model B Rev 1.2 (4GB RAM)"
        # Add newer models as they're released and documented.
    }

    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith('Revision'):
                revision = line.split(":")[1].strip().lower()
                model = revisions.get(revision, "Unknown Model")
                return {"code": revision, "description": model}
    return {"code": "N/A", "description": "Unknown Model"}


def memory_info():
    """Return memory usage information."""
    memory = psutil.virtual_memory()

    total_mem = memory.total / (1024 ** 2)  # Convert bytes to MB
    available_mem = memory.available / (1024 ** 2)
    used_mem = memory.used / (1024 ** 2)
    memory_percentage = memory.percent

    return f"Total Memory: {total_mem:.2f} MB, Used: {used_mem:.2f} MB, Available: {available_mem:.2f} MB, Usage: {memory_percentage}%"


def cpu_info():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('model name'):
                    return line.strip().split(":")[1].strip()
        return "Unknown"
    except Exception:
        return "Error fetching CPU info."


def sd_card_performance():
    # This will measure a simple write and read performance. It's not comprehensive.
    try:
        write_speed = subprocess.getoutput("dd if=/dev/zero of=tempfile bs=1M count=1024 conv=fdatasync,notrunc")
        read_speed = subprocess.getoutput("dd if=tempfile of=/dev/null bs=1M count=1024")
        os.remove("tempfile")
        return (write_speed.split()[-1], read_speed.split()[-1])
    except Exception:
        return ("Error measuring write speed", "Error measuring read speed")

def ethernet_port_status():
    try:
        # 1. Check if the eth0 interface exists
        interfaces_output = subprocess.getoutput('ls /sys/class/net')
        if 'eth0' not in interfaces_output:
            return "Ethernet interface (eth0) not found."

        # 2. Check link detection for eth0
        link_detected_output = subprocess.getoutput('cat /sys/class/net/eth0/carrier')
        if link_detected_output.strip() == "0":
            return "Ethernet interface (eth0) is present but no link detected."

        # 3. Check the ability to communicate over the network with a simple ping
        ping_google = subprocess.run(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ping_google.returncode == 0:
            return "Ethernet interface (eth0) is functional and has internet connectivity."
        else:
            return "Ethernet interface (eth0) is present, link detected but no internet connectivity."

    except Exception as e:
        return f"Error checking Ethernet status: {e}"


def ethernet_speed():
    try:
        # Run speedtest-cli and get JSON output
        speedtest_output = subprocess.getoutput('speedtest-cli --json')
        speedtest_data = json.loads(speedtest_output)

        download_speed_mbps = speedtest_data["download"] / 1_000_000  # Convert from bits to Mbps
        upload_speed_mbps = speedtest_data["upload"] / 1_000_000      # Convert from bits to Mbps
        ping = speedtest_data["ping"]

        return (f"Download Speed: {download_speed_mbps:.2f} Mbps",
                f"Upload Speed: {upload_speed_mbps:.2f} Mbps",
                f"Ping: {ping} ms")
    except Exception as e:
        return (f"Error running speedtest-cli: {e}", "", "")

def wifi_adapter_status():
    try:
        # 1. Check if the wlan0 interface exists
        interfaces_output = subprocess.getoutput('ls /sys/class/net')
        if 'wlan0' not in interfaces_output:
            return "WiFi interface (wlan0) not found."

        # 2. Scan for available networks. Requires the user to be in the 'netdev' group or running as root.
        scan_output = subprocess.getoutput('sudo iwlist wlan0 scan')
        if 'No scan results' in scan_output:
            return "WiFi interface (wlan0) is present but can't detect networks. Ensure WiFi is enabled and permissions are set."

        # 3. Check if the adapter is connected to a network
        connection_check = subprocess.getoutput('iwconfig wlan0 | grep "ESSID:off/any"')
        if 'ESSID:off/any' in connection_check:
            connection_status = "Not connected to any WiFi network."
        else:
            connection_status = "Connected to a WiFi network."

        # 4. Check the ability to communicate over the network with a simple ping
        ping_google = subprocess.run(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ping_google.returncode == 0:
            internet_status = "Has internet connectivity."
        else:
            internet_status = "No internet connectivity."

        return f"WiFi interface (wlan0) is functional. {connection_status} {internet_status}"

    except Exception as e:
        return f"Error checking WiFi status: {e}"

def wifi_availability():
    try:
        output = subprocess.getoutput('iwconfig 2>&1 | grep "no wireless"')
        return "Not available" if "no wireless" in output else "Available"
    except Exception:
        return "Error checking wifi."


def bluetooth_availability():
    try:
        output = subprocess.getoutput('hcitool dev')
        return "Available" if "hci" in output else "Not available"
    except Exception:
        return "Error checking bluetooth."


def usb_ports():
    # This will check for USB devices. The presence of devices doesn't guarantee functionality.
    try:
        output = subprocess.getoutput('lsusb')
        return output
    except Exception:
        return "Error checking USB ports."

def usb_ports_test():
    base_path = '/sys/bus/usb/devices'
    usb_ports = [dir for dir in os.listdir(base_path) if dir.startswith("usb")]

    if not usb_ports:
        return "No USB ports found."

    usb_status = {}

    for port in usb_ports:
        port_path = os.path.join(base_path, port)
        try:
            # Check if there's a product file. This generally means a device is connected.
            with open(os.path.join(port_path, 'product'), 'r') as f:
                device_name = f.read().strip()
            usb_status[port] = f"Device connected: {device_name}"
        except FileNotFoundError:
            usb_status[port] = "No device connected"

    readable_output = "\n".join([f"Port {port}: {status}" for port, status in usb_status.items()])
    return readable_output


def gpio_pins():
    # Placeholder: This will only inform about the presence based on Raspberry Pi version.
    version = raspberry_pi_version()
    # Refer to official Raspberry Pi documentation for GPIO pin count per version.
    pin_info = {
        "a02082": (3, 40),  # Example: Pi 3 Model B
    }
    return pin_info.get(version, ("Unknown model", "Unknown pin count"))
def gpio_pins_test():
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setwarnings(False)   # Turn off warnings

    # Typically, Raspberry Pi models have GPIO pins ranging from GPIO2 to GPIO27.
    # Adjust the range if your model is different.
    pins_range = list(range(2, 28))

    failed_pins = []

    for pin in pins_range:
        try:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            GPIO.setup(pin, GPIO.IN)
            if not GPIO.input(pin):  # If we can't read HIGH after setting to HIGH, it's a failure.
                failed_pins.append(pin)
        except Exception as e:
            failed_pins.append(pin)

    GPIO.cleanup()

    if not failed_pins:
        return "All GPIO pins are functioning correctly."
    else:
        return f"GPIO pins with potential issues: {', '.join(map(str, failed_pins))}"

import subprocess
import os


def camera_port_test():
    try:
        # Try capturing a test image
        test_image_path = "/tmp/test_image.jpg"
        capture_process = subprocess.run(['raspistill', '-o', test_image_path, '-t', '1'], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, timeout=10)

        # If the capture succeeds, the camera is working.
        if capture_process.returncode == 0 and os.path.exists(test_image_path):
            image_size = os.path.getsize(test_image_path)
            os.remove(test_image_path)  # Clean up the test image
            return f"Camera is functioning correctly. Test image size: {image_size} bytes."

        # If capturing fails, check the error to determine the reason.
        elif "not detected" in capture_process.stderr.decode("utf-8"):
            return "No camera detected on the camera port."

        else:
            return f"Camera capture failed with error: {capture_process.stderr.decode('utf-8')}"

    except subprocess.TimeoutExpired:
        return "Camera capture timed out. Check if the camera module is functioning correctly."

    except Exception as e:
        return f"Error during camera test: {e}"


def display_port_test():
    try:
        # Check if DSI display is connected using DRM
        if not is_dsi_display_connected():
            return "No display detected on the DSI port. If you're using a non-official screen, manual inspection is recommended."

        # Display a test pattern using pygame with feedback
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 480))
        screen.fill((255, 0, 0))
        font = pygame.font.Font(None, 36)
        text_surface = font.render("If you see this, press any key.", True, (255, 255, 255))
        screen.blit(text_surface, (100, 240))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting_for_input = False

        pygame.quit()
        return "A display appears to be connected to the DSI port."

    except Exception as e:
        return f"Error during display port test: {e}"


def is_dsi_display_connected():
    return os.path.exists('/sys/class/drm/card0-DSI-1/status') and \
        open('/sys/class/drm/card0-DSI-1/status').read().strip() == 'connected'


def hdmi_port_test():
    try:
        # Check if HDMI display is connected using DRM
        if not is_hdmi_display_connected():
            return "HDMI port is not active or no monitor is detected."

        # Display a test pattern using pygame with feedback on HDMI
        import pygame
        pygame.init()
        info = pygame.display.Info()  # Get current screen resolution
        screen = pygame.display.set_mode((info.current_w, info.current_h),
                                         pygame.FULLSCREEN)  # Use current resolution in fullscreen
        screen.fill((0, 255, 0))  # Fill screen with green color
        font = pygame.font.Font(None, 36)
        text_surface = font.render("If you see this on HDMI, press any key.", True, (255, 255, 255))
        screen.blit(text_surface, (info.current_w // 4, info.current_h // 2))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting_for_input = False

        pygame.quit()

        return f"A display appears to be connected to the HDMI port. A green test pattern was displayed on a screen with resolution {info.current_w}x{info.current_h}."

    except Exception as e:
        return f"Error during HDMI port test: {e}"


def is_hdmi_display_connected():
    # Usually, Raspberry Pi's HDMI outputs are labeled HDMI-A-1 and HDMI-A-2
    for hdmi_output in ['HDMI-A-1', 'HDMI-A-2']:
        if os.path.exists(f'/sys/class/drm/card0-{hdmi_output}/status') and \
                open(f'/sys/class/drm/card0-{hdmi_output}/status').read().strip() == 'connected':
            return True
    return False


def audio_jack_test():
    try:
        # Check the current audio output using amixer
        amixer_output = subprocess.getoutput('amixer cget numid=3')
        if "values=1" not in amixer_output:
            # Switch to audio jack output
            subprocess.run(['amixer', 'cset', 'numid=3', '1'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Play a test sound (assuming a .wav file named 'test_sound.wav' is present in the current directory)
        subprocess.run(['aplay', 'test_sound.wav'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Provide results and instructions
        results = [
            "Attempted to play a test sound through the audio jack.",
            "Please confirm if the sound played correctly from connected speakers or headphones."
        ]

        return "\n".join(results)

    except subprocess.CalledProcessError as e:
        return f"Error during audio jack test: {e.output.decode('utf-8')}"

    except Exception as e:
        return f"Error during audio jack test: {e}"

def get_cpu_temperature():
    """Return CPU temperature."""
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
        # Read the temperature and convert it from millidegrees to degrees Celsius.
        temp_c = int(temp_file.read()) / 1000.0
    return f"CPU Temperature: {temp_c}°C"


def get_cpu_voltage():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_voltage", "r") as f:
            cpu_voltage = f.readline().strip()
            return f"CPU Voltage: {cpu_voltage} V"
    except FileNotFoundError:
        return "Cannot retrieve CPU voltage. File not found."
    except Exception as e:
        return f"Error retrieving CPU voltage: {e}"

def get_voltages():
    cpu_voltage = get_cpu_voltage()
    # We can't get exact values for other voltages without vcgencmd
    # Placeholders:
    sdram_c_voltage = "Unavailable"
    sdram_i_voltage = "Unavailable"
    sdram_p_voltage = "Unavailable"
    return f"Core Voltage (CPU): {cpu_voltage}\nSDRAM_C Voltage: {sdram_c_voltage}\nSDRAM_I Voltage: {sdram_i_voltage}\nSDRAM_P Voltage: {sdram_p_voltage}"

def get_cpu_utilization():
    utilization = psutil.cpu_percent()
    return f"CPU Utilization: {utilization}%"

def get_gpu_memory():
    try:
        with open("/boot/config.txt", "r") as file:
            for line in file.readlines():
                if line.startswith("gpu_mem="):
                    memory = line.split("=")[1].strip()
                    return f"GPU Memory: {memory}M"
        return "GPU Memory info not found in /boot/config.txt."
    except FileNotFoundError:
        return "Cannot retrieve GPU memory. /boot/config.txt not found."
    except Exception as e:
        return f"Error retrieving GPU memory: {e}"


def get_clock_frequencies():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
            arm_freq_khz = int(f.readline().strip())  # Read the frequency in KHz
            arm_freq_mhz = arm_freq_khz / 1000  # Convert to MHz

        # Since the GPU and Core frequencies aren't exposed through sysfs by default,
        # we'll indicate that in the output.
        return f"ARM Clock Frequency: {arm_freq_mhz} MHz\nGPU Clock Frequency: Not Available\nCore Clock Frequency: Not Available"

    except FileNotFoundError:
        return "Error: CPU frequency path not found."
    except Exception as e:
        return f"Error retrieving clock frequencies: {e}"


def get_disk_io():
    io_counters = psutil.disk_io_counters(perdisk=False)
    return f"Disk Read Count: {io_counters.read_count}\nDisk Write Count: {io_counters.write_count}\nBytes Read: {io_counters.read_bytes}\nBytes Written: {io_counters.write_bytes}"

def get_hardware_codecs():
    # Map of codec names to their potential corresponding kernel modules.
    # Note: This mapping might not be perfect and may need adjustments based on Raspberry Pi model and OS version.
    codecs_map = {
        'MPG2': 'mpeg2_v4l2_m2m',
        'WVC1': None,  # As of my last update, there's no direct kernel module for WVC1
        'VP8': 'vp8_v4l2_m2m',
        'VP9': 'vp9_v4l2_m2m',
        'H264': 'h264_v4l2_m2m',
        'MJPG': 'mjpeg_v4l2_m2m'
    }

    results = []
    for codec, module in codecs_map.items():
        if module:
            # Check if the module is loaded
            module_status = subprocess.getoutput(f"lsmod | grep {module}")
            if module_status:
                results.append(f"{codec} codec is enabled.")
            else:
                results.append(f"{codec} codec is not enabled.")
        else:
            results.append(f"{codec} codec status cannot be determined.")

    return '\n'.join(results)

def get_irq_statistics():
    with open("/proc/interrupts", "r") as f:
        return '\n'.join(f.readlines()[:10])

def get_network_stats():
    return subprocess.getoutput("netstat -i")

def get_bluetooth_info():
    return subprocess.getoutput("hciconfig")

def get_storage_space():
    return subprocess.getoutput("df -h")

def get_uptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.read().split()[0])
        uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
        return f"Uptime: {uptime_str}"



if __name__ == "__main__":
    test_results = master_test()
