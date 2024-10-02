#!/bin/bash

HOST="paffenroth-23.dyn.wpi.edu"
USER="student-admin"
LOGFILE="ssh_test.log"

# Attempt SSH connection using the key
if ssh -o BatchMode=yes -p 22001 -i student-admin_key -o  ConnectTimeout=5 "$USER@$HOST" "exit" &> /dev/null; then
    echo "$(date): SSH connection successful" >> "$LOGFILE"

    #run setupmachine
    echo "Running setupmachineafterrestart.sh"
    ./setupmachineafterrestart.sh
    echo "Finished running setupmachineafterrestart.sh"

    echo "Initialize model"
    ./runmodel.sh
else
    echo "$(date): SSH connection failed" >> "$LOGFILE"
fi
