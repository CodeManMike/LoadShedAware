#!/usr/bin/env python3

# Import necessary modules
import datetime
import re
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Module 'bs4' not found. Please install it using 'pip install beautifulsoup4' command.")
    exit()

def parse_schedule():
    """
    Parse the load shedding schedule from an HTML file.

    This function reads an HTML file containing a load shedding schedule,
    extracts the times of the shutdowns, and returns the next shutdown time.
    If there is no next shutdown time, it returns None.

    Returns:
        datetime.datetime: The next shutdown time if it exists, otherwise None.
    """
    # Open the HTML file
    with open("load_shedding_schedule.html", "r", encoding='utf-8') as f:
        contents = f.read()

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the schedule on the webpage
    schedule_text = soup.get_text()

    # Use regex to find the times
    times = re.findall(r'\d{2}:\d{2} - \d{2}:\d{2}', schedule_text)

    # Convert the times to datetime objects and subtract 10 minutes
    shutdown_times = []
    for time in times:
        start_time, _ = time.split(' - ')
        date_time = datetime.datetime.strptime(start_time, "%H:%M")
        date_time -= datetime.timedelta(minutes=10)
        shutdown_times.append(date_time)  # Append the date_time to shutdown_times list

    # Sort the shutdown times
    shutdown_times.sort()

    # Get the current time
    now = datetime.datetime.now()

    # Find the next shutdown time
    for time in shutdown_times:
        if time > now:
            return time

    # If there is no next shutdown time, return None
    return None

if __name__ == "__main__":
    next_shutdown_time = parse_schedule()
    if next_shutdown_time is not None:
        print(next_shutdown_time.strftime("%H:%M"))
    else:
        print("No loadshedding scheduled today! YAY!")

