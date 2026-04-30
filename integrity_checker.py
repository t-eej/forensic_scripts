import glob
import hashlib
import json
import os
import sys


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None


def get_files_from_pattern(pattern):
    """Expands wildcards and returns a list of valid files."""
    # recursive=True allows '**/*' patterns for subdirectories
    return [f for f in glob.glob(pattern, recursive=True) if os.path.isfile(f)]


def create_baseline(pattern, baseline_file):
    results = {}
    files = get_files_from_pattern(pattern)
    print(f"[*] Scanning pattern: {pattern}")

    for path in files:
        file_hash = calculate_sha256(path)
        if file_hash:
            results[path] = file_hash
            print(f"[+] Hashed: {path}")

    with open(baseline_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"[!] Baseline complete. {len(results)} files tracked.")


def verify_integrity(pattern, baseline_file):
    if not os.path.exists(baseline_file):
        print(f"[-] Baseline file {baseline_file} not found.")
        return

    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    files = get_files_from_pattern(pattern)
    print(f"[*] Verifying against pattern: {pattern}")

    # Track which baseline files we've seen to detect deletions
    seen_in_scan = []

    for path in files:
        seen_in_scan.append(path)
        current_hash = calculate_sha256(path)

        if path not in baseline:
            print(f"[NEW FILE] {path}")
        elif current_hash != baseline[path]:
            print(f"[MODIFIED] {path}")

    # Check for deletions
    for path in baseline:
        if path not in seen_in_scan:
            print(f"[DELETED] {path}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(script_dir, "test_files/**/*")
    baseline_path = os.path.join(script_dir, "baseline.json")

    if len(sys.argv) < 2:
        print("Usage: python3 integrity_checker.py [baseline|verify]")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "baseline":
        create_baseline(target_dir, baseline_path)
    elif mode == "verify":
        verify_integrity(target_dir, baseline_path)
    else:
        print(f"Invalid mode: {mode}. Use 'baseline' or 'verify'.")
