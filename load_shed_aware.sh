#!/bin/bash

# Create a file called config.sh and add the following lines to it:
# #!/bin/bash
# Your Pushbullet API key
# export API_KEY="YOUR_PUSHBULLET_API_KEY"

# Import the API key
if [ -f ./config.sh ]; then
    source ./config.sh
else
    echo "config.sh file does not exist."
    exit 1
fi

# Fetch the load shedding schedule
echo "Fetching the load shedding schedule..."
if [ -f ./fetch_schedule.sh ]; then
    ./fetch_schedule.sh
else
    echo "fetch_schedule.sh file does not exist."
    exit 1
fi

# Check if the fetch_schedule.sh script was successful
if [ $? -eq 0 ]
then
    echo "Schedule fetched successfully."
else
    echo "Failed to fetch schedule."
    ./send_notification.sh "error" "Failed to fetch schedule."
    exit 1
fi

# Parse the schedule and schedule the shutdown
echo "Parsing the schedule and scheduling the shutdown..."
if [ -f ./schedule_shutdown.sh ]; then
    ./schedule_shutdown.sh
else
    echo "schedule_shutdown.sh file does not exist."
    exit 1
fi

# Check if the schedule_shutdown.sh script was successful
if [ $? -eq 0 ]
then
    echo "Shutdown scheduled successfully."
else
    echo "Failed to schedule shutdown."
    ./send_notification.sh "error" "Failed to schedule shutdown."
    exit 1
fi

# Send a notification
echo "Sending a notification..."
if [ -f ./send_notification.sh ]; then
    ./send_notification.sh
else
    echo "send_notification.sh file does not exist."
    exit 1
fi

# Check if the send_notification.sh script was successful
if [ $? -eq 0 ]
then
    echo "Notification sent successfully."
else
    echo "Failed to send notification."
    exit 1
fi

echo "All tasks completed successfully."

