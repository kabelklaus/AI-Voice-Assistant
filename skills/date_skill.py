# date_skill.py

import locale
from datetime import datetime

# Set locale to German
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

def get_current_date():
    today = datetime.now()
    return today.strftime("%A, der %d. %B %Y")

def get_current_week():
    today = datetime.now()
    week_number = today.strftime("%W")
    return f"Kalenderwoche {week_number}"

def get_current_day():
    today = datetime.now()
    return today.strftime("%A")