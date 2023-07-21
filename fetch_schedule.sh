#!/bin/bash

# URL of the webpage containing the load shedding schedule
URL="https://www.ourpower.co.za/areas/city-of-cape-town/hout-bay?block=11"

# Use curl to fetch the webpage
curl -o load_shedding_schedule.html $URL

# Check if the curl command was successful
if [ $? -eq 0 ]
then
    echo "Webpage fetched successfully."
else
    echo "Failed to fetch webpage."
    exit 1
fi
