```python
#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime

def parse_schedule():
    # Open the HTML file
    with open("load_shedding_schedule.html", "r") as f:
        contents = f.read()

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the schedule on the webpage
    schedule = soup.find(id="schedule")

    # Extract the times from the schedule
    times = schedule.find_all("time")

    # Convert the times to datetime objects and subtract 10 minutes
    shutdown_times = []
    for time in times:
        dt = datetime.datetime.strptime(time.text, "%H:%M")
        dt -= datetime.timedelta(minutes=10)
        shutdown_times.append(dt)

    # Return the shutdown times
    return shutdown_times

if __name__ == "__main__":
    shutdown_times = parse_schedule()
    for time in shutdown_times:
        print(time.strftime("%H:%M"))
```
