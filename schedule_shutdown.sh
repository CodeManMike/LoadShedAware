#!/bin/bash

# Cancel any previously scheduled shutdown
sudo shutdown -c

# Import the parsed schedule times
shutdown_times=$(python3 parse_schedule.py)

# Check if the python script executed successfully
if [ $? -ne 0 ]
then
    echo "Failed to parse schedule."
    exit 1
fi

# Loop through each shutdown time
for time in $shutdown_times
do
    # Convert the time to the format required by the shutdown command
    shutdown_time=$(date -d "$time" +"%H:%M")

    # Check if the date command was successful
    if [ $? -ne 0 ]
    then
        echo "Failed to convert time."
        continue
    fi

    # Schedule the shutdown
    echo "Scheduling shutdown for $shutdown_time"
    sudo shutdown -h $shutdown_time
    
    # Check if the shutdown command was successful
    if [ $? -ne 0 ]
    then
        echo "Failed to schedule shutdown."
        continue
    fi

    # Send a notification about the new schedule
    ./send_notification.sh "schedule" "$shutdown_time"

    # Check if the notification command was successful
    if [ $? -ne 0 ]
    then
        echo "Failed to send notification."
        continue
    fi

    # Schedule a notification 10 minutes before shutdown
    alert_time=$(date -d "$shutdown_time - 10 minutes" +"%H:%M")
    echo "Scheduling alert for $alert_time"
    echo "./send_notification.sh 'alert' '$shutdown_time'" | at $alert_time

    # Check if the at command was successful
    if [ $? -ne 0 ]
    then
        echo "Failed to schedule alert."
        continue
    fi
done

