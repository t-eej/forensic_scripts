#!/bin/bash
LOG_FILE=$1

echo "--- TOP 5 SUSPICIOUS IPs ---"
awk '{print $3}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 5

echo -e "\n--- RECENT 403 FORBIDDEN ERRORS ---"
grep "403" "$LOG_FILE" | tail -n 5
