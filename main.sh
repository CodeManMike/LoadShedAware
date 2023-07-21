```bash
#!/bin/bash

# Create a file called config.sh and add the following lines to it:
# #!/bin/bash
# Your Pushbullet API key
# export API_KEY="YOUR_PUSHBULLET_API_KEY"

# Import the API key
source ./config.sh

# Fetch the load shedding schedule
echo "Fetching the load shedding schedule..."
./fetch_schedule.sh

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
./schedule_shutdown.sh

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
./send_notification.sh

# Check if the send_notification.sh script was successful
if [ $? -eq 0 ]
then
    echo "Notification sent successfully."
else
    echo "Failed to send notification."
    exit 1
fi

echo "All tasks completed successfully."
```
