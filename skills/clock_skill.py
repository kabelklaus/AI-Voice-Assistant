# clock_skill.py

from datetime import datetime

def get_current_time():
    now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    current_time = now.strftime("%H:%M")
    return f"{current_time} Uhr"
