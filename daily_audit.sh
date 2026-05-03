#!/bin/bash
LOG=$1

if [ -z "$LOG" ]; then
    echo "Usage: ./daily_audit.sh <logfile>"
    exit 1
fi

echo "=========================================="
echo "   SHIELD-V1 LOG AUDIT REPORT             "
echo "   Date: $(date)"
echo "=========================================="
echo ""

# Running the modules locally
bash ./find-brute "$LOG"
echo ""
bash ./find-errors "$LOG"
echo ""
bash ./check-payload "$LOG"

echo ""
echo "=========================================="
echo "   AUDIT COMPLETE"
echo "=========================================="
