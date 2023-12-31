import subprocess
import json
import os


def run_script(script_name):
    os.system(f"python3 {script_name}")


def capture_script_output(script_name):
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    return result.stdout


def display_human_readable(test_results):
    if not test_results:
        print("No results to display. Exiting.")
        return
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
    run_script("dependencies_check.py")  # This will allow user interaction
    test_results = capture_script_output("diagnostics.py")

    if not test_results:
        print("No test results obtained. Exiting.")
        exit()

    choice = input("Do you want the output in a human-readable form (h/human) or as JSON (j/json)? ").strip().lower()
    if choice in ['human', 'h']:
        display_human_readable(test_results)
    elif choice in ['json', 'j']:
        print(test_results)
    else:
        print("Invalid choice. Exiting.")
        exit()