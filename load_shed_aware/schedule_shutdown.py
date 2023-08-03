"""
This module contains functions to fetch the current load shedding stage, 
fetch the load shedding schedule based on the area name, and schedule the system shutdown.
"""
import datetime
import os
import json
import requests
from dateutil.parser import parse
from dotenv import load_dotenv
from .send_notification import send_notification

load_dotenv()

# Headers for the API requests
headers = {
    'token': os.environ.get('ESP_API_KEY'),
}

def fetch_current_stage():
    """
    Fetches the current load shedding stage from the API.

    Returns:
        current_stage (int): The current load shedding stage.
        next_stage (int): The next load shedding stage.
        next_stage_start (datetime): The start time of the next stage.
    """
    response = requests.get(
        'https://developer.sepush.co.za/business/2.0/status', headers=headers, timeout=10)
    status = json.loads(response.text)['status']['capetown']
    current_stage = int(status['stage'])

    # Get the next stage and its start time
    next_stage_info = status['next_stages'][0]
    next_stage = int(next_stage_info['stage'])
    next_stage_start = parse(next_stage_info['stage_start_timestamp'])

    return current_stage, next_stage, next_stage_start


def fetch_schedule(area_name):
    """
    Fetches the load shedding schedule for a given area from the API.

    Args:
        area_name (str): The name of the area to fetch the schedule for.

    Returns:
        schedule (dict): The load shedding schedule for the area.
    """
    response = requests.get('https://developer.sepush.co.za/business/2.0/area',
                            headers=headers, params={'id': area_name}, timeout=10)
    schedule = json.loads(response.text)
    return schedule


def schedule_shutdown(schedule, current_stage, next_stage, next_stage_start):
    """
    Parses the load shedding schedule and schedules a system shutdown based on the current stage.

    Args:
        schedule (dict): The load shedding schedule.
        current_stage (int): The current load shedding stage.
        next_stage (int): The next load shedding stage.
        next_stage_start (datetime): The start time of the next stage.
    """
    # Parse the schedule based on the current stage
    today = datetime.date.today()
    today_schedule = next((item for item in schedule['schedule']['days']
                           if parse(item['date']).date() == today), None)

    # Check if there's a schedule for today
    if today_schedule is None:
        send_notification("schedule", "No schedule for today.")
        return

    # Get the time slots for the current stage
    time_slots = today_schedule['stages'][current_stage - 1]

    # Get the current time
    now = datetime.datetime.now().time()

    # Check if the current time falls within any of the load shedding time slots
    for time_slot in time_slots:
        start_time, end_time = map(
            lambda t: datetime.datetime.strptime(t, '%H:%M').time(), time_slot.split('-'))
        if start_time <= now <= end_time:
            # Emergency shutdown
            send_notification("schedule", "Emergency shutdown due to current load shedding.")
            os.system('sudo shutdown -h now')
            return

    # Determine the next shutdown time
    for time_slot in time_slots:
        start_time, end_time = map(
            lambda t: datetime.datetime.strptime(t, '%H:%M').time(), time_slot.split('-'))

        # If the next stage will start before or on the next scheduled shutdown,
        # switch to the new stage
        if next_stage_start.time() <= start_time:
            current_stage = next_stage
            time_slots = today_schedule['stages'][current_stage - 1]

        # If the current time is before the start time of the time slot,
        # schedule the shutdown for the start time
        if now < start_time:
            shutdown_time = start_time
            break
    else:
        # If there are no more load shedding times for today,
        # check if the next day's load shedding time is midnight
        tomorrow_schedule = next(
            (item for item in schedule['schedule']['days']
            if parse(item['date']).date() == today + datetime.timedelta(days=1)),None)
        if tomorrow_schedule is not None:
            time_slots_tomorrow_current_stage = tomorrow_schedule['stages'][current_stage - 1]
            time_slots_tomorrow_next_stage = tomorrow_schedule['stages'][next_stage - 1]

            if (time_slots_tomorrow_current_stage[0].split('-')[0] == '00:00' or 
                time_slots_tomorrow_next_stage[0].split('-')[0] == '00:00'):
                shutdown_time = datetime.datetime.combine(today, datetime.time(23, 50))
            else:
                send_notification("schedule", "No more load shedding times for today.")
                return
        else:
            send_notification("schedule", "No more load shedding times for today.")
            return

    # Convert the time to the format required by the shutdown command
    shutdown_time = shutdown_time.strftime('%H:%M')

    # Schedule the system shutdown
    os.system(f'sudo shutdown -h {shutdown_time}')

    # Send a notification about the new schedule
    send_notification("schedule", shutdown_time)

        # Schedule a notification 10 minutes before shutdown
    alert_time = (datetime.datetime.strptime(shutdown_time, "%H:%M") 
                  - datetime.timedelta(minutes=10)).strftime("%H:%M")
    command = f'echo "./send_notification.py \'alert\' \'{shutdown_time}\'" | at {alert_time}'
    os.system(command)
