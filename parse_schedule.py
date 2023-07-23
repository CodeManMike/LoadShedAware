#!/usr/bin/env python3
"""
This module parses a load shedding schedule from an HTML file.
"""

# Import necessary modules
import datetime
import re
import sys
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Module 'bs4' not found. Please install it using 'pip install beautifulsoup4' command.")
    sys.exit()

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
    with open("load_shedding_schedule.html", "r", encoding='utf-8') as file:
        contents = file.read()

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the schedule on the webpage
    schedule_text = soup.get_text()

    # Use regex to find the dates
    dates = re.findall(r'\d{2} \w+', schedule_text)

    # Use regex to find the times
    times = re.findall(r'\d{2}:\d{2} - \d{2}:\d{2}', schedule_text)

    # Get the current date and time
    now = datetime.datetime.now()

    # Initialize the current date
    current_date = now.date()

    # Convert the dates and times to datetime objects and subtract 10 minutes
    shutdown_times = []
    for date, time in zip(dates, times):
        # Update the current date if a new date is found
        new_date = datetime.datetime.strptime(date + ' ' + str(now.year), "%d %B %Y").date()
        if new_date != current_date:
            current_date = new_date

        start_time, _ = time.split(' - ')
        start_time_obj = datetime.datetime.strptime(start_time, "%H:%M").time()
        date_time_obj = datetime.datetime.combine(current_date, start_time_obj)
        date_time_obj -= datetime.timedelta(minutes=10)
        shutdown_times.append(date_time_obj)  # Append the date_time_obj to shutdown_times list

    # Sort the shutdown times
    shutdown_times.sort()

    # Find the next shutdown time
    for time in shutdown_times:
        if time > now:
            return time

    # If there is no next shutdown time, return None
    return None

if __name__ == "__main__":
    next_shutdown_time = parse_schedule()
    if next_shutdown_time is not None:
        print(next_shutdown_time.strftime("%Y-%m-%d %H:%M"))
    else:
        print("No loadshedding scheduled today! YAY!")
