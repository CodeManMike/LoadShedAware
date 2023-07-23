#!/bin/bash

# Cancel any previously scheduled shutdown
sudo shutdown -c

# Import the parsed schedule times
shutdown_time=$(python3 parse_schedule.py)

# Check if the python script executed successfully
if [ $? -ne 0 ]
then
    echo "Failed to parse schedule."
    exit 1
fi

# Check if there is a shutdown time
if [ "$shutdown_time" == "No loadshedding scheduled today! YAY!" ]
then
    echo "$shutdown_time"
    ./send_notification.sh "schedule" "$shutdown_time"
    exit 0
fi

# Convert the time to the format required by the shutdown command
shutdown_time=$(date -d "$shutdown_time" +"%H:%M")

# Check if the date command was successful
if [ $? -ne 0 ]
then
    echo "Failed to convert time."
    exit 1
fi

# Schedule the shutdown
echo "Scheduling shutdown for $shutdown_time"
sudo shutdown -h $shutdown_time

# Check if the shutdown command was successful
if [ $? -ne 0 ]
then
    echo "Failed to schedule shutdown."
    exit 1
fi

# Send a notification about the new schedule
./send_notification.sh "schedule" "$shutdown_time"

# Check if the notification command was successful
if [ $? -ne 0 ]
then
    echo "Failed to send notification."
    exit 1
fi

# Schedule a notification 10 minutes before shutdown
alert_time=$(date -d "$shutdown_time - 10 minutes" +"%H:%M")
echo "Scheduling alert for $alert_time"
echo "./send_notification.sh 'alert' '$shutdown_time'" | at $alert_time

# Check if the at command was successful
if [ $? -ne 0 ]
then
    echo "Failed to schedule alert."
    exit 1
fi
