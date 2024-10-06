#!/bin/bash


# scp -i student-admin_key -P 22001 allpublickeys student-admin@paffenroth-23.dyn.wpi.edu

# scp -i student-admin_key -P 22001 sharedkey.pub student-admin@paffenroth-23.dyn.wpi.edu

scp -i student-admin_key -P 22001 karate_key.pub student-admin@paffenroth-23.dyn.wpi.edu:~
sudo ssh -i student-admin_key -p 22001 student-admin@paffenroth-23.dyn.wpi.edu

echo "Creating new user karate7800"
sudo useradd -m karate7800 
sudo -u karate7800 mkdir -p /home/karate7800/.ssh
sudo cp /home/student-admin/karate_key.pub /home/karate7800/.ssh/authorized_keys

sudo chown -R karate7800 /home/karate7800/.ssh
sudo chmod 600 /home/karate7800/.ssh/authorized_keys

echo "Added SSH KEY"

