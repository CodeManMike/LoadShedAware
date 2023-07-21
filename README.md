# Load Shedding Schedule Fetcher and Notifier

This project is a Linux server service script that fetches a load shedding schedule from a webpage, parses the schedule to extract the load shedding times, schedules a server shutdown 10 minutes before the actual load shedding time, and sends a notification to your phone using the Pushbullet API.

## Files

- `fetch_schedule.sh`: Fetches the webpage containing the load shedding schedule.
- `parse_schedule.py`: Parses the fetched webpage to extract the load shedding times.
- `schedule_shutdown.sh`: Schedules a server shutdown 10 minutes before the actual load shedding time.
- `send_notification.sh`: Sends a notification to your phone using the Pushbullet API.
- `main.sh`: The main script that runs all the other scripts.
- `requirements.txt`: Contains the Python libraries required for the project.

## Requirements

- Python 3
- BeautifulSoup4
- curl or wget
- Pushbullet API key

## Installation

1. Clone the repository.
2. Install the required Python libraries by running `pip install -r requirements.txt`.
3. Replace `YOUR_PUSHBULLET_API_KEY` in `send_notification.sh` with your actual Pushbullet API key.

## Usage

Run the main script with `./main.sh`.

## Scripts

### fetch_schedule.sh

This script fetches the webpage containing the load shedding schedule using curl.

### parse_schedule.py

This Python script parses the fetched webpage to extract the load shedding times. It uses BeautifulSoup to parse the HTML and find the schedule.

### schedule_shutdown.sh

This script schedules a server shutdown 10 minutes before the actual load shedding time. It uses the shutdown command in Linux to schedule the shutdown.

### send_notification.sh

This script sends a notification to your phone using the Pushbullet API. It sends a POST request to the Pushbullet API with your message.

### main.sh

This is the main script that runs all the other scripts. It first fetches the load shedding schedule, then parses the schedule, schedules the shutdown, and finally sends the notification.

## Note

Please ensure that you have the necessary permissions to run the scripts and schedule a shutdown on your server.
