# calendar_utils.py
import json
from datetime import datetime, timedelta

CALENDAR_FILE = "./data/calendar.json"

def load_calendar():
    try:
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_calendar(calendar):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(calendar, f, indent=2)

def generate_daily_slots(start="10:00", end="16:00", interval=30):
    slots = {}
    current = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    while current < end_time:
        slots[current.strftime("%H:%M")] = None
        current += timedelta(minutes=interval)
    return slots

def ensure_day_exists(calendar, date_str):
    if date_str not in calendar:
        calendar[date_str] = generate_daily_slots()
    return calendar

def book_slot(username, date_str, time_str):
    calendar = load_calendar()
    calendar = ensure_day_exists(calendar, date_str)

    if calendar[date_str].get(time_str) is None:
        calendar[date_str][time_str] = username
        save_calendar(calendar)
        return True, f"Appointment booked on {date_str} at {time_str}."
    else:
        return False, f"Sorry, {time_str} on {date_str} is already taken."

def list_user_appointments(username):
    calendar = load_calendar()
    appointments = []
    for date, slots in calendar.items():
        for time, user in slots.items():
            if user == username:
                appointments.append(f"{date} at {time}")
    return appointments