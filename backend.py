import os
import json
from datetime import datetime, date

class Tasks():

    def __init__(self):
        self.tasks = []
        if not os.path.exists('saves/tasks.json'):
            self.tasks.append({
                'name': 'My Task',
                'time': '1 hour',
                'day': 'monday',
                'month': 'may',
                'type': 'Personal',
                'description': 'This is a sample task'
            })
        self.load_tasks()

    def add_task(self, name, time, day, month, type, description):
        new_task = {
            'name': name,
            'time': time,
            'day': day,
            'month': month,
            'type': type,
            'description': description,
        }
        self.tasks.append(new_task)

    def get_tasks(self):
        return self.tasks

    def save_task(self):
        try:
            with open('saves/tasks.json', 'w') as file:
                json.dump(self.tasks, file)
            print("Tasks saved successfully.")
        except IOError as e:
            print(f"An error occurred while saving tasks: {e}")

    def load_tasks(self):
        if os.path.exists('saves/tasks.json'):
            with open('saves/tasks.json', 'r') as file:
                try:
                    self.tasks = json.load(file)
                except json.JSONDecodeError as e:  # Correct exception for JSON files
                    print(f"An error occurred while loading tasks: {e}")
                    self.tasks = []  # Fallback to an empty list if loading fails
        else:
            self.tasks = []  # Create an empty list if the file doesn't exist

class TimeManager:

    @staticmethod
    def populate_days(month, year):
        days = [str(day) for day in range(1, date(year, month, 1).days_in_month + 1)]
        return days

    def populate_months(self):
        return["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    def populate_time(self):
        hours = [str(hour).zfill(2) for hour in range(24)]
        minutes = [str(minute).zfill(2) for minute in range(60)]
        times = []
        for hour in hours:
            for minute in minutes:
                times.append(f"{hour}:{minute}")
        return times

