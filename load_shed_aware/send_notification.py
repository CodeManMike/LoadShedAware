"""
This module is used to send notifications related to load shedding events.
It uses the Pushbullet API to send these notifications.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_notification(notification_type, message):
    """
    Sends a notification based on the type and message provided.

    Args:
        notification_type (str): The type of notification to send. 
        Can be "schedule", "alert", or "error".
        message (str): The message to include in the notification.

    Returns:
        str: The response from the Pushbullet API or 
        an error message if the notification type is invalid.
    """
    if notification_type == "schedule":
        message = "New shutdown scheduled for " + message
    elif notification_type == "alert":
        message = "Server will shutdown at " + message + " due to load shedding."
    elif notification_type == "error":
        message = "Error: " + message
    else:
        return "Invalid notification type."

    response = requests.post(
    'https://api.pushbullet.com/v2/pushes',
    headers={'Access-Token': os.environ.get('PUSH_API_KEY'), 'Content-Type': 'application/json'},
    json={'type': 'note', 'title': 'Server Shutdown Alert', 'body': message},
    timeout=5
)
    return response
