#!/bin/bash

# 1. Safety Check: Ensure we are actually on the SSD
# Replace 'forensic_toolkit' with the actual name of your SSD mount
if [[ "$PWD" != *"/forensic_toolkit"* ]]; then
    echo "[-] Error: You are not on the SSD. Navigate to your SSD first."
    exit 1
fi

echo "[*] Generating robust test data in: $PWD/test_files"

# 2. Create the base directory
mkdir -p test_files
cd test_files

# 3. The Nested Loop
for i in {1..3}; do
    # Create nested directories to test your "**/*" logic
    DIR="folder_$i/subfolder_$i"
    mkdir -p "$DIR"

    # Create an empty file (Tests 0-byte file hashing)
    touch "$DIR/empty_file.txt"

    # Create a file with actual text
    echo "This is evidence file $i" > "$DIR/evidence_$i.log"

    # Create a 'large' file (1MB) of random data
    # This ensures your 4096-byte chunk loop is actually working
    head -c 1M </dev/urandom > "$DIR/random_sample_$i.bin"
done

echo "[+] Data generation complete."
