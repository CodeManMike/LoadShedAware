#!/bin/bash

# Your Pushbullet API key
API_KEY="o.NiOxAT2etmvDD9y7UuT59wTOU7hguZYc"

# Prepare the message based on the type of notification
notification_type=$1
message=$2

# Check if the notification type and message are not empty
if [ -z "$notification_type" ] || [ -z "$message" ]; then
    echo "Notification type and message cannot be empty."
    exit 1
fi

if [ "$notification_type" == "schedule" ]; then
    message="New shutdown scheduled for $message"
elif [ "$notification_type" == "alert" ]; then
    message="Server will shutdown at $message due to load shedding."
elif [ "$notification_type" == "error" ]; then
    message="Error: $message"
else
    echo "Invalid notification type."
    exit 1
fi

# Send the notification
echo "Sending notification: $message"
response=$(curl -s -u $API_KEY: -X POST https://api.pushbullet.com/v2/pushes --header 'Content-Type: application/json' --data-binary "{\"type\": \"note\", \"title\": \"Server Shutdown Alert\", \"body\": \"$message\"}")

# Check if the curl command was successful
if [ $? -eq 0 ]
then
    echo "Notification sent successfully."
else
    echo "Failed to send notification."
    exit 1
fi

# Check if the response contains an error
if echo "$response" | grep -q "error"; then
    echo "Error in response: $response"
    exit 1
fi

