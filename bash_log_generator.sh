#!/bin/bash

# Define some "Attacker" variables
IPS=("192.168.1.15" "10.0.0.42" "172.16.0.5" "192.168.1.100")
USERS=("root" "admin" "db_user" "guest" "backdoor")
LOG_FILE="fake_auth.log"

echo "[*] Generating 100 fake failed login attempts..."

# Create/Clear the file
> $LOG_FILE

for i in {1..100}; do
    # Pick a random IP and User from our lists
    RAND_IP=${IPS[$RANDOM % ${#IPS[@]}]}
    RAND_USER=${USERS[$RANDOM % ${#USERS[@]}]}
    RAND_PORT=$((RANDOM % 64000 + 1024))

    # Randomly decide if the user is "invalid"
    INVALID=""
    if [ $((RANDOM % 2)) -eq 0 ]; then
        INVALID="invalid user "
    fi

    # Write the formatted line
    echo "Apr 30 01:00:00 pop-os sshd[1234]: Failed password for $INVALID$RAND_USER from $RAND_IP port $RAND_PORT ssh2" >> $LOG_FILE
done

echo "[+] $LOG_FILE created with 100 entries."
