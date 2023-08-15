import subprocess
import json
import os


def run_script(script_name):
    os.system(f"python3 {script_name}")


def capture_script_output(script_name):
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    return result.stdout


def display_human_readable(test_results):
    parsed_results = json.loads(test_results)
    for key, value in parsed_results.items():
        print(f"{key}:\n{'-' * len(key)}")
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(value)
        print("=" * 40)


if __name__ == "__main__":
    run_script("dependencies_check.py")
    test_results = capture_script_output("diagnostics.py")

    choice = input(
        "Do you want the output in a human-readable form or as JSON? (Enter 'human' or 'json'): ").strip().lower()
    if choice == 'human':
        display_human_readable(test_results)
    elif choice == 'json':
        print(test_results)
    else:
        print("Invalid choice. Exiting.")