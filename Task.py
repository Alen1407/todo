from tkinter import messagebox

from datetime import datetime, timedelta


class Task:
    def __init__(self, name, description, due_date, status="Not Completed"):
        self.name = name
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        self.status = status
        self.notification_sent = False
        self.check_due_date()

    def check_due_date(self):
        remaining_time = self.due_date - datetime.now()

        if remaining_time < timedelta(days=1) and not self.notification_sent:
            messagebox.showwarning("Task Deadline Approaching", f"The task '{self.name}' is due soon!")
            self.notification_sent = True

        if remaining_time < timedelta(seconds=0):
            self.status = "Overdue"

    def __str__(self):
        return f"Name: {self.name}\nDescription: {self.description}\nDue Date: {self.due_date}\nStatus: {self.status}"

