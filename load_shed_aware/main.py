"""
This module is responsible for fetching the current load shedding stage and schedule, 
scheduling the system shutdown, and sending a notification.
"""

import os
from dotenv import load_dotenv
from .schedule_shutdown import fetch_current_stage, fetch_schedule, schedule_shutdown
from .send_notification import send_notification

load_dotenv()

def main():
    """
    Main function to fetch the current load shedding stage and schedule, 
    schedule the system shutdown and send a notification.
    """
    # Fetch the current load shedding stage and schedule
    current_stage, next_stage, next_stage_start = fetch_current_stage()
    schedule = fetch_schedule(os.environ.get('AREA'))  # replace with actual area name

    # Schedule the system shutdown
    schedule_shutdown(schedule, current_stage, next_stage, next_stage_start)

    # Send a notification
    send_notification("schedule", "Shutdown scheduled successfully.")
