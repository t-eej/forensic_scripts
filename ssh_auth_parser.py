import glob
import os
import re
from collections import Counter


def parse_ssh_auth_log(pattern):
    # Using a regular expression to find failed logins and snapshot the User and IP
    failed_pattern = r"Failed password for (invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+) port (\d+) ssh2"

    ip_list = []
    user_list = []
    port_list = []
    log_files = glob.glob(pattern)

    if not log_files:
        print(f"[-] No log files found matching pattern: {pattern}")
        return
    print(f"[*] Found {len(log_files)} files to analyze.")

    # Loop through each log file and parse it using wildcards
    for log_file in log_files:
        print(f"    [+] Processing: {log_file}")
        try:
            with open(log_file, "r") as f:
                for line in f:
                    match = re.search(failed_pattern, line)
                    if match:
                        user_list.append(match.group(2))
                        ip_list.append(match.group(3))
                        port_list.append(match.group(4))
        except PermissionError:
            print(f"    [-] Permission denied: {log_file}")

    user_counter = Counter(user_list)
    ip_counter = Counter(ip_list)
    port_counter = Counter(port_list)

    print(f"[+] User counter: {user_counter}")
    print(f"[+] Port counter: {port_counter}")
    print(f"\n{'IP Address':<20} | {'Attempts':<10}")
    print("-" * 35)
    for ip, count in ip_counter.items():
        alert = " [!!!] POSSIBLE BRUTE FORCE" if count > 5 else ""
        print(f"{ip:<20} | {count:<10} {alert}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_pattern = os.path.join(script_dir, "*.log")

    parse_ssh_auth_log(target_pattern)
