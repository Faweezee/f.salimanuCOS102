from datetime import datetime
from tkinter import messagebox as msgbox
from task import Task
from db_operations import Database
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class TaskManager:
    """Manages task operations and coordinates UI and database."""
    def __init__(self):
        self.db = Database()
        self.db.create_tables()

    def login(self, username, password):
        """Authenticates user credentials."""
        logger.info(f"Attempting login for username={username}")
        return self.db.authenticate_user(username, password)

    def register(self, username, password):
        """Registers a new user."""
        logger.info(f"Attempting registration for username={username}")
        return self.db.insert_user(username, password)

    def validate_task_input(self, title, description, priority, deadline, duration):
        """Validates task input fields."""
        if not title or not deadline or not duration:
            msgbox.showerror("Missing Entries", "Please fill in all non-optional fields")
            logger.error("Missing required fields: title, deadline, or duration")
            return False
        if priority not in ["High", "Medium", "Low"]:
            msgbox.showerror("Error", "Priority must be High, Medium, or Low")
            logger.error(f"Invalid priority: {priority}")
            return False
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            msgbox.showerror("Error", "Duration must be a positive integer")
            logger.error(f"Invalid duration: {duration}")
            return False
        try:
            deadline_datetime = datetime.strptime(deadline, "%d/%m/%Y %I:%M %p")
        except ValueError:
            msgbox.showerror("Error", "Deadline format: DD/MM/YYYY HH:MM AM/PM")
            logger.error(f"Invalid deadline format: {deadline}")
            return False
        return (title, description, priority, deadline, deadline_datetime, duration)

    def add_task(self, main_window, user_id, title, description, priority, deadline, duration):
        """Adds a new task."""
        validated = self.validate_task_input(title, description, priority, deadline, duration)
        if not validated:
            return
        title, description, priority, deadline, deadline_datetime, duration = validated
        task_id = self.db.insert_task(title, description, priority, deadline, deadline_datetime, duration, user_id)
        if task_id:
            Task(task_id, title, description, priority, deadline, deadline_datetime, duration)
            logger.info(f"Inserted task_id={task_id} for user_id={user_id}")
            msgbox.showinfo("Success", "Task added successfully")
            main_window._update_listboxes()
        else:
            msgbox.showerror("Error", "Failed to add task")
            logger.error(f"Failed to insert task for user_id={user_id}")

    def edit_task(self, main_window, user_id, task_id, title, description, priority, deadline, duration):
        """Edits an existing task."""
        if task_id is None:
            msgbox.showwarning("Warning", "Please select a task to edit")
            logger.warning("No task selected for edit")
            return
        
        validated = self.validate_task_input(title, description, priority, deadline, duration)
        if not validated:
            return
        title, description, priority, deadline, deadline_datetime, duration = validated
        if self.db.update_task(task_id, title, description, priority, deadline, deadline_datetime, duration, user_id):
            logger.info(f"Updated task_id={task_id} for user_id={user_id}")
            msgbox.showinfo("Success", "Task updated successfully")
            main_window._update_listboxes()
        else:
            msgbox.showerror("Error", f"Failed to update task with task_id={task_id}")
            logger.error(f"Failed to update task_id={task_id} for user_id={user_id}")

    def open_edit_task(self, main_window, user_id, task_id):
        """Opens the edit task form with pre-filled data."""
        if task_id is None:
            msgbox.showwarning("Warning", "Please select a task to edit")
            logger.warning("No task selected for edit")
            return
        tasks = self.db.fetch_tasks(user_id)
        selected_task = None
        for task in tasks:
            if task[0] == task_id:
                selected_task = {
                    "id": task[0], "title": task[1], "description": task[2],
                    "priority": task[3], "deadline_str": task[4], "duration": task[5]
                }
                break
        if selected_task:
            from gui import TaskFormWindow
            TaskFormWindow(main_window, user_id, self, selected_task)
        else:
            msgbox.showerror("Error", f"Task with ID {task_id} not found")
            logger.error(f"Task_id={task_id} not found for user_id={user_id}")

    def delete_task(self, main_window, user_id, task_id):
        """Deletes a selected task."""
        if task_id is None:
            msgbox.showwarning("Warning", "Please select a task to delete")
            logger.warning("No task selected for deletion")
            return
        logger.info(f"Attempting to delete task_id={task_id} for user_id={user_id}")
        if self.db.delete_task(task_id, user_id):
            msgbox.showinfo("Success", "Task deleted successfully")
            main_window._update_listboxes()
        else:
            msgbox.showerror("Error", f"Failed to delete task with task_id={task_id}")
            logger.error(f"Failed to delete task_id={task_id} for user_id={user_id}")

    def get_tasks(self, user_id, sort_option="By Deadline"):
        """Fetches tasks with sorting."""
        logger.info(f"Fetching tasks for user_id={user_id}, sort={sort_option}")
        try:
            tasks = self.db.fetch_tasks(user_id, sort_option)
            if not tasks:
                logger.info(f"No tasks found for user_id={user_id}")
            return tasks
        except Exception as e:
            logger.exception(f"Error fetching tasks for user_id={user_id}: {e}")
            return []