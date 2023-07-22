#!/bin/bash

# URL of the webpage containing the load shedding schedule
URL="https://www.ourpower.co.za/areas/city-of-cape-town/hout-bay?block=11"

# Check if URL is empty
if [ -z "$URL" ]
then
    echo "URL is empty."
    exit 1
fi

# Use curl to fetch the webpage
curl -o load_shedding_schedule.html $URL

# Check if the curl command was successful
if [ $? -ne 0 ]
then
    echo "Failed to fetch webpage."
    exit 1
else
    echo "Webpage fetched successfully."
fi

