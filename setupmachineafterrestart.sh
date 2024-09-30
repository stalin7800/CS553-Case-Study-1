#!/bin/bash

# NEW_USER = "karate7800"


if [ -z "$1" ]; then
    echo "Usage: $0 <key>"
    exit 1
fi
    
key=$1

git clone https://github.com/stalin7800/CS553-Case-Study-1 


sudo scp -i student-admin_key -P 22001 -r CS553-Case-Study-1 student-admin@paffenroth-23.dyn.wpi.edu:~
scp -i student-admin_key -P 22001 karate_key.pub student-admin@paffenroth-23.dyn.wpi.edu:~
scp -i student-admin_key -P 22001 case2_key.pub student-admin@paffenroth-23.dyn.wpi.edu:~

# cat ../karate_key.pub >> authorized_keys
sudo ssh -i student-admin_key -p 22001 student-admin@paffenroth-23.dyn.wpi.edu "rm .ssh/authorized_keys;cat karate_key.pub >> .ssh/authorized_keys;cat case2_key.pub >> .ssh/authorized_keys"


#install python3-venv and install requirements
ssh -i karate_key -p 22001 student-admin@paffenroth-23.dyn.wpi.edu "sudo apt install -qq -y python3-venv && cd CS553-Case-Study-1 && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"


#run 


# ADD SHARE=TRUE
# UPDATE REQUIREMENT>TXT

# echo "Adding karate_key.pub to authorized_keys"

# cd .ssh
# # cat 