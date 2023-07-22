#!/bin/bash

# Update package lists for upgrades and new package installations
sudo apt-get update

# Install Python3 and pip3 if they are not installed
sudo apt-get install -y python3 python3-pip

# Read the requirements.txt file line by line
while read package; do
    # Check if the package is installed
    pip3 show $package > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$package is already installed"
    else
        echo "Installing $package"
        pip3 install $package
    fi
done < requirements.txt

# Make all .sh files executable
chmod +x *.sh

echo "Setup completed successfully."