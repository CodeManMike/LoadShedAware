```bash
#!/bin/bash

# Import the parsed schedule times
shutdown_times=$(python3 parse_schedule.py)

# Loop through each shutdown time
for time in $shutdown_times
do
    # Convert the time to the format required by the shutdown command
    shutdown_time=$(date -d "$time" +"%H:%M")

    # Schedule the shutdown
    echo "Scheduling shutdown for $shutdown_time"
    sudo shutdown -h $shutdown_time
done

# Check if the shutdown command was successful
if [ $? -eq 0 ]
then
    echo "Shutdown scheduled successfully."
else
    echo "Failed to schedule shutdown."
    exit 1
fi
```
