from tkinter import messagebox, END
from tkinter import ttk
from datetime import datetime, timedelta
from Task import Task
import threading
import time

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("600x400")

        # Create styles
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        # Create task entry components
        self.create_task_entry(self.root)

        # Create buttons
        self.create_button("Add Task", self.add_task_gui, 5, 0)
        self.create_button("Delete Task", self.delete_task_gui, 5, 1)
        self.create_button("Change Status", self.change_status_gui, 6, 0)
        self.create_button("Change Due Date", self.change_due_date_gui, 6, 1)
        self.create_button("Mark Completed", self.mark_completed_gui, 7, 0)
        self.create_button("Display Tasks", self.display_tasks_gui, 7, 1)

        # Todo list
        self.tasks = []

        # Start the task checker thread
        self.start_task_checker()

    def add_task_gui(self):
        name = self.task_name_entry.get()
        description = self.task_desc_entry.get()
        due_date = self.due_date_entry.get()

        if name and description and due_date:
            task = Task(name, description, due_date)
            self.tasks.append(task)

            messagebox.showinfo("Task Added", "Task added successfully!")
            self.clear_entries()

    def delete_task_gui(self):
        name = self.task_name_entry.get()

        if name:
            for task in self.tasks:
                if task.name == name:
                    self.tasks.remove(task)
                    break

            messagebox.showinfo("Task Deleted", "Task deleted successfully!")
            self.clear_entries()

    def change_status_gui(self):
        name = self.task_name_entry.get()
        status = self.task_status_entry.get()

        if name and status:
            for task in self.tasks:
                if task.name == name:
                    task.status = status
                    break

            messagebox.showinfo("Task Status Changed", "Task status changed successfully!")
            self.clear_entries()

    def change_due_date_gui(self):
        name = self.task_name_entry.get()
        due_date = self.due_date_entry.get()

        if name and due_date:
            for task in self.tasks:
                if task.name == name:
                    task.due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
                    break

            messagebox.showinfo("Due Date Changed", "Task due date changed successfully!")
            self.clear_entries()

    def mark_completed_gui(self):
        name = self.task_name_entry.get()

        if name:
            for task in self.tasks:
                if task.name == name:
                    task.status = "Completed"
                    break

            messagebox.showinfo("Task Marked Completed", "Task marked as completed successfully!")
            self.clear_entries()

    def display_tasks_gui(self):
        text = ""
        for task in self.tasks:
            text += str(task) + "\n\n"

        messagebox.showinfo("Task List", text)

    def create_task_entry(self, root):
        self.task_name_label = self.create_label("Task Name:", 0, 0)
        self.task_name_entry = self.create_entry(0, 1)

        self.task_desc_label = self.create_label("Task Description:", 1, 0)
        self.task_desc_entry = self.create_entry(1, 1)

        self.due_date_label = self.create_label("Due Date (YYYY-MM-DD HH:MM):", 2, 0)
        self.due_date_entry = self.create_entry(2, 1)

        self.task_status_label = self.create_label("Task Status:", 3, 0)
        self.task_status_entry = self.create_entry(3, 1)

    def create_label(self, text, row, column):
        label = ttk.Label(self.root, text=text)
        label.grid(row=row, column=column, sticky="W", padx=10, pady=5)
        return label

    def create_entry(self, row, column):
        entry = ttk.Entry(self.root, width=30)
        entry.grid(row=row, column=column, padx=10, pady=5)
        return entry

    def create_button(self, text, command, row, column):
        button = ttk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=column, padx=10, pady=5)

    def clear_entries(self):
        self.task_name_entry.delete(0, END)
        self.task_desc_entry.delete(0, END)
        self.due_date_entry.delete(0, END)
        self.task_status_entry.delete(0, END)

    def start_task_checker(self):
        thread = threading.Thread(target=self.task_checker)
        thread.start()

    def task_checker(self):
        while True:
            for task in self.tasks:
                task.check_due_date()

            time.sleep(60)
