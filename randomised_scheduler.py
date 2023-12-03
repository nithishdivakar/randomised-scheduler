from croniter import croniter
import datetime
from collections import defaultdict
import random


def generate_random_for_date(input_date):
    date_str = input_date.strftime("%Y-%m-%d")
    random.seed(date_str)
    random_number = random.random()
    return random_number

def get_current_week():
    today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    return start_of_week, end_of_week

def parse_schedules(schedules):
    parsed_schedules = {}
    for schedule in schedules:
        parts = schedule.split()
        cron_expression = " ".join(parts[:5])
        probability = float(parts[5])
        task_name = " ".join(parts[6:])

        parsed_schedules[task_name] = {
            "cron": cron_expression,
            "prob": probability
        }
    return parsed_schedules


SCHEDULES = [
    # * * * * *
    # | | | | |
    # | | | | +---- Day of the week (0 - 7) (Sunday is 0 or 7, Monday is 1, and so on)
    # | | | +------ Month (1 - 12)
    # | | +-------- Day of the month (1 - 31)
    # | +---------- Hour (0 - 23)
    # +------------ Minute (0 - 59)

    "0 0 * * mon-sat 0.5 Yoga",
    "0 0 * * mon-sat 0.5 Workout",
    "0 0 * * mon-sat 0.166 Paper reading",
    "0 0 * * mon-sat 0.166 Internal Document Reading",
    "0 0 * * wed 1.0 Task 3",
    "0 0 * * wed 0.5 Task 4",
    "0 0 * * sat#1,sun#2 1.0 Task 5",
    "0 0 * * 5#3,L5 1.0 Task 6",
]

parsed_schedules = parse_schedules(SCHEDULES)

start_date,_ = get_current_week()
for days_delta in range(10):
    current_date = start_date + datetime.timedelta(days=days_delta)
    P = generate_random_for_date(current_date)
    print(f"""\n# {current_date.strftime("%a %Y-%m-%d").upper().strip()}""",P)

    for task, schedule in parsed_schedules.items():
        if croniter.match(schedule['cron'], current_date) and P <= schedule['prob']:
            print(f"  - [ ] {task}")


    
  
