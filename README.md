# Load Shedding Schedule Fetcher and Notifier

This project is a Linux server service script that fetches a load shedding schedule from a webpage, parses the schedule to extract the load shedding times, schedules a server shutdown 10 minutes before the actual load shedding time, and sends a notification to your phone using the Pushbullet API.

## Files

- `fetch_schedule.sh`: Fetches the webpage containing the load shedding schedule and checks if the webpage was fetched successfully. It uses curl to fetch the webpage and checks if the URL is empty before fetching.
- `parse_schedule.py`: Parses the fetched webpage to extract the load shedding times and converts the times to datetime objects. It uses BeautifulSoup to parse the HTML and find the schedule. It then uses regex to find the times and converts the times to datetime objects, subtracting 10 minutes.
- `schedule_shutdown.sh`: Cancels any previously scheduled shutdown, schedules a new shutdown at the parsed times, and sends a notification about the new schedule. It also schedules a notification 10 minutes before shutdown.
- `send_notification.sh`: Prepares the message based on the type of notification and sends the notification using the Pushbullet API. It checks if the notification type and message are not empty before sending.
- `load_shed_aware.sh`: The main script that runs all the other scripts. It fetches the load shedding schedule, parses the schedule, schedules the shutdown, sends the notification, and checks if each step was successful.
- `requirements.txt`: Contains the Python libraries required for the project.

## Requirements

- Python 3
- BeautifulSoup4
- curl or wget
- Pushbullet API key

## Installation

1. Clone the repository.
2. Install the required Python libraries by running `pip install -r requirements.txt`.
3. Create a file called `config.sh` and add the following lines to it:
    ```bash
    #!/bin/bash
    # Your Pushbullet API key
    export API_KEY="YOUR_PUSHBULLET_API_KEY"
    ```
    Replace `YOUR_PUSHBULLET_API_KEY` with your actual Pushbullet API key.
    You can sign up for this for free. Just do a search for Pushbullet.

## Usage

Run the main script with `./load_shed_aware.sh`.

To automate the script, add a cron job by running `crontab -e` and adding the following line:

    ```bash
    0 * * * * /path/to/load_shed_aware.sh
    ```

Now, your script will check the site every hour, update its scheduled shutdown, remove the old scheduled shutdown, and send a notification. It will also run as a service. Feel free to alter the timing.

The basic format of a cron schedule expression consists of 5 fields, separated by spaces, in the following order:

1. Minute (0 - 59)
2. Hour (0 - 23)
3. Day of the month (1 - 31)
4. Month (1 - 12)
5. Day of the week (0 - 7) (Sunday = 0 or 7)

Each field can have a single value, a range of values (e.g., 1-5 for Monday to Friday), or an asterisk (which means "any value").

## Note

Please ensure that you have the necessary permissions to run the scripts and schedule a shutdown on your server.

## License

This project is licensed under the terms of the MIT License. This means you can freely use, modify, distribute, and sell this software, as long as you include the original copyright notice and disclaimers. 

In practice, this means that if you use this software in your own work, you need to acknowledge me, @CodeManMike, as the original author of the software.

Here's an example of how you might do this:

"This software uses code from the project Load Shedding Schedule Fetcher and Notifier by @CodeManMike (https://github.com/CodeManMike/LoadSheddingScheduleFetcherAndNotifier)."

Remember, while this license allows you to freely use and modify the software, it comes with no warranties. I am not liable for anything that happens as a result of your use of this software.

