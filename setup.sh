#!/bin/bash

# Update package lists for upgrades and new package installations
sudo apt-get update

# Install Python3 and pip3 if they are not installed
sudo apt-get install -y python3 python3-pip

# Install the required Python libraries
pip3 install -r requirements.txt

# Make all .sh files executable
chmod +x *.sh

echo "Setup completed successfully."