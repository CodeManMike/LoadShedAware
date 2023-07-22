#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime
import re

def parse_schedule():
    # Open the HTML file
    with open("load_shedding_schedule.html", "r") as f:
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
        start_time, end_time = time.split(' - ')
        dt = datetime.datetime.strptime(start_time, "%H:%M")
        dt -= datetime.timedelta(minutes=10)
        shutdown_times.append(dt)

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
