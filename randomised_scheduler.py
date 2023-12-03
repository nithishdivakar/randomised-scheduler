from croniter import croniter
import datetime
from collections import defaultdict
import random
import argparse

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

def read_file_ignore_comments(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        cleaned_lines = [line.strip() for line in lines if not line.strip().startswith('#')]
        cleaned_lines = [line for line in cleaned_lines if line] # remove empty lines
    return cleaned_lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Randomised Task Scheduler')
    parser.add_argument('--file', type=str, default="example_schedule.txt", help='Name of the file to read')

    args = parser.parse_args()

    file_name = args.file
    schedules = read_file_ignore_comments(file_name)

    parsed_schedules = parse_schedules(schedules)

    start_date,_ = get_current_week()
    for days_delta in range(14):
        current_date = start_date + datetime.timedelta(days=days_delta)
        P = generate_random_for_date(current_date)
        print(f"""\n# {current_date.strftime("%a %Y-%m-%d").upper().strip()}""",P)

        for task, schedule in parsed_schedules.items():
            if croniter.match(schedule['cron'], current_date) and P <= schedule['prob']:
                print(f"  - [ ] {task}")


    
  
