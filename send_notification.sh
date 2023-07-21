```bash
#!/bin/bash

# Import the parsed schedule times
shutdown_times=$(python3 parse_schedule.py)

# Your Pushbullet API key
API_KEY="YOUR_PUSHBULLET_API_KEY"

# Loop through each shutdown time
for time in $shutdown_times
do
    # Convert the time to the format required by the shutdown command
    shutdown_time=$(date -d "$time" +"%H:%M")

    # Prepare the message
    message="Server will shutdown at $shutdown_time due to load shedding."

    # Send the notification
    echo "Sending notification for shutdown at $shutdown_time"
    curl -u $API_KEY: -X POST https://api.pushbullet.com/v2/pushes --header 'Content-Type: application/json' --data-binary "{\"type\": \"note\", \"title\": \"Server Shutdown Alert\", \"body\": \"$message\"}"
done

# Check if the curl command was successful
if [ $? -eq 0 ]
then
    echo "Notification sent successfully."
else
    echo "Failed to send notification."
    exit 1
fi
```
