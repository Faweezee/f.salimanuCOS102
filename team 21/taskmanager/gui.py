import tkinter as tk
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from task_manager import TaskManager
import logging
from datetime import datetime

# Configure logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def configure_styles():
    """Configure consistent Tkinter widget styles."""
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme for button visibility
    style.configure(
        "TButton",
        font=("Helvetica", 12),
        padding=10,
        foreground="#000000",
        background="#d3d3d3"
    )
    style.map(
        "TButton",
        foreground=[('active', '#000000'), ('disabled', '#666666')],
        background=[('active', '#b0b0b0'), ('disabled', '#e0e0e0')]
    )
    style.configure("TCombobox", font=("Helvetica", 12))
    style.configure(
        "Sidebar.TButton",
        font=("Helvetica", 12, "bold"),
        padding=10,
        foreground="#ffffff",
        background="#5e81ac"  # Blue sidebar buttons
    )
    style.map(
        "Sidebar.TButton",
        foreground=[('active', '#ffffff'), ('disabled', '#cccccc')],
        background=[('active', '#4a6a8c'), ('disabled', '#7a9ccc')]
    )
    return style

class LoginWindow:
    """Manages the login/registration UI."""
    def __init__(self, root, on_success):
        logger.info("Initializing LoginWindow")
        self.root = root
        self.window = tk.Toplevel(root)  # Create login window
        self.window.geometry("400x300")
        self.window.title("Task Manager - Login")
        self.window.configure(bg="#f0f2f5")  # Light background
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        self.on_success = on_success
        self.task_manager = TaskManager()
        self._setup_ui()

    def _setup_ui(self):
        """Configures login window widgets."""
        configure_styles()
        header = tk.Label(
            self.window, text="Task Manager", font=("Helvetica", 20),
            bg="#f0f2f5", fg="#2c3e50"
        )
        header.pack(pady=20)

        frame = tk.Frame(self.window, bg="#f0f2f5")
        frame.pack(pady=10)

        tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = ttk.Entry(frame, width=25, font=("Helvetica", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Password:", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = ttk.Entry(frame, width=25, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        button_frame = tk.Frame(self.window, bg="#f0f2f5")
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Login", command=self._login, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Register", command=self._register, style="TButton").grid(row=0, column=1, padx=5)

    def _login(self):
        """Handles login attempt."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            tkMessageBox.showerror("Error", "Please fill in both fields")
            logger.error("Empty username or password")
            return
        logger.info(f"Attempting login for username={username}")
        try:
            user_id = self.task_manager.login(username, password)
            if user_id:
                logger.info(f"Logged in user_id={user_id}")
                self._close_and_proceed(user_id)
            else:
                tkMessageBox.showerror("Error", "Invalid username or password")
                logger.error(f"Login failed for username={username}")
        except Exception as e:
            tkMessageBox.showerror("Error", f"Login error: {e}")
            logger.exception(f"Login exception: {e}")

    def _register(self):
        """Handles user registration."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            tkMessageBox.showerror("Error", "Please fill in both fields")
            logger.error("Empty username or password")
            return
        logger.info(f"Attempting registration for username={username}")
        try:
            user_id = self.task_manager.register(username, password)
            if user_id:
                logger.info(f"Registered user_id={user_id}")
                self._close_and_proceed(user_id)
            else:
                tkMessageBox.showerror("Error", "Registration failed")
                logger.error(f"Registration failed for username={username}")
        except Exception as e:
            tkMessageBox.showerror("Error", f"Registration error: {e}")
            logger.exception(f"Registration exception: {e}")

    def _close_and_proceed(self, user_id):
        """Closes login window and proceeds to main window."""
        logger.info("Closing LoginWindow")
        try:
            self.window.update()
            self.window.destroy()
            self.on_success(user_id)
        except Exception as e:
            logger.exception(f"Error closing LoginWindow: {e}")
            raise

    def _on_close(self):
        """Handles login window close button."""
        logger.info("LoginWindow close button clicked")
        self.root.quit()

    def run(self):
        """Starts login window event loop."""
        logger.info("Starting LoginWindow")
        self.window.grab_set()
        self.root.wait_window(self.window)
        

class TaskFormWindow:
    """Manages the add/edit task form UI."""
    def __init__(self, main_window, user_id, task_manager, task=None):
        logger.info(f"Initializing TaskFormWindow with user_id={user_id}")
        self.window = tk.Toplevel(main_window.window)
        self.window.geometry("650x450")
        self.window.title("Edit Task" if task else "Add Task")
        self.window.configure(bg="#f0f2f5")
        self.window.resizable(False, False)

        self.main_window = main_window
        self.user_id = user_id
        self.task_manager = task_manager
        self.task = task
        self.priority_var = tk.StringVar(value="Low" if not task else task.get("priority", "Low"))
        self._setup_ui()

    def _setup_ui(self):
        """Configures task form widgets."""
        configure_styles()
        tk.Label(
            self.window, text="Edit Task" if self.task else "Add New Task",
            font=("Helvetica", 18),
            bg="#f0f2f5", fg="#2c3e50"
        ).pack(pady=20)

        frame = tk.Frame(self.window, bg="#f0f2f5")
        frame.pack(pady=10, padx=20, fill="x")

        tk.Label(frame, text="Title:", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = ttk.Entry(frame, width=40, font=("Helvetica", 12))
        if self.task:
            self.title_entry.insert(0, self.task.get("title", ""))
        self.title_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Description (optional):", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.description_text = tk.Text(frame, height=4, width=40, font=("Helvetica", 12))
        if self.task and self.task.get("description"):
            self.description_text.insert("1.0", self.task["description"])
        self.description_text.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Priority:", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        priority_menu = ttk.Combobox(frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], font=("Helvetica", 12), state="readonly")
        priority_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Deadline (DD/MM/YYYY HH:MM AM/PM):", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.deadline_entry = ttk.Entry(frame, width=40, font=("Helvetica", 12))
        if self.task:
            self.deadline_entry.insert(0, self.task.get("deadline_str", ""))
        self.deadline_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(frame, text="Duration (minutes):", font=("Helvetica", 12), bg="#f0f2f5", fg="#34495e").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.duration_entry = ttk.Entry(frame, width=40, font=("Helvetica", 12))
        if self.task:
            self.duration_entry.insert(0, str(self.task.get("duration", "")))
        self.duration_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(
            self.window, text="Save Changes" if self.task else "Add Task",
            command=self._submit, style="TButton"
        ).pack(pady=20)

    def _submit(self):
        """Submits task data for add/edit."""
        try:
            title = self.title_entry.get().strip()
            description = self.description_text.get("1.0", "end").strip()
            priority = self.priority_var.get()
            deadline = self.deadline_entry.get().strip()
            duration = self.duration_entry.get().strip()

            logger.info(f"Submitting task: title={title}, priority={priority}")
            if self.task:
                self.task_manager.edit_task(
                    self.main_window, self.user_id, self.task["id"],
                    title, description, priority, deadline, duration
                )
            else:
                self.task_manager.add_task(
                    self.main_window, self.user_id,
                    title, description, priority, deadline, duration
                )
            self.window.destroy()
        except Exception as e:
            tkMessageBox.showerror("Error", f"Failed to submit task: {e}")
            logger.exception(f"Task submission error: {e}")


class MainWindow:
    """Manages the main task manager UI with task list and controls."""
    def __init__(self, root, user_id, on_logout):
        logger.info(f"Initializing MainWindow with user_id={user_id}")
        self.window = root
        self.window.geometry("980x500")
        self.window.title("Task Manager")
        self.window.configure(bg="#f0f2f5")
        self.window.resizable(False, False)

        self.user_id = user_id
        self.on_logout = on_logout
        self.task_manager = TaskManager()
        self.selected_task_id = None
        self.selected_task_index = None
        self.is_syncing_selection = False
        self.task_ids = []

        try:
            self._setup_ui()
            self.window.deiconify()
            self.window.update()
            self._update_listboxes()
            self._start_deadline_check()  # Start periodic deadline checks
        except Exception as e:
            logger.exception(f"MainWindow initialization error: {e}")
            tkMessageBox.showerror("Error", f"Failed to initialize main window: {e}")
            self.window.destroy()
            raise

    def _setup_ui(self):
        """Configures main window layout with sidebar and task listboxes."""
        logger.info("Setting up MainWindow UI")
        try:
            configure_styles()
            # Sidebar for navigation
            sidebar = tk.Frame(self.window, bg="#2c3e50", width=200)
            sidebar.pack(side="left", fill="y")
            sidebar.pack_propagate(False)

            tk.Label(
                sidebar, text="Menu", font=("Helvetica", 16),
                bg="#2c3e50", fg="#ffffff"
            ).pack(pady=20)

            ttk.Button(
                sidebar, text="Add Task", command=self._open_add_task,
                style="Sidebar.TButton"
            ).pack(fill="x", padx=10, pady=5)

            ttk.Button(
                sidebar, text="Edit Task", command=self._open_edit_task,
                style="Sidebar.TButton"
            ).pack(fill="x", padx=10, pady=5)

            ttk.Button(
                sidebar, text="Delete Task", command=self._delete_task,
                style="Sidebar.TButton"
            ).pack(fill="x", padx=10, pady=5)

            # Sorting options
            tk.Label(
                sidebar, text="Sort Tasks", font=("Helvetica", 12),
                bg="#2c3e50", fg="#ffffff"
            ).pack(pady=10, padx=10, anchor="w")
            self.sort_var = tk.StringVar(value="By Deadline")
            sort_menu = ttk.Combobox(
                sidebar, textvariable=self.sort_var, values=["By Priority", "By Deadline"],
                font=("Helvetica", 12), state="readonly"
            )
            sort_menu.pack(fill="x", padx=10, pady=5)
            sort_menu.bind("<<ComboboxSelected>>", lambda e: self._update_listboxes())

            ttk.Button(
                sidebar, text="Logout", command=self._logout,
                style="Sidebar.TButton"
            ).pack(fill="x", padx=10, pady=5)

            # Main content area
            content = tk.Frame(self.window, bg="#f0f2f5")
            content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

            tk.Label(
                content, text="Task Manager", font=("Helvetica", 24),
                bg="#f0f2f5", fg="#2c3e50"
            ).pack(pady=10)

            list_frame = tk.Frame(content, bg="#f0f2f5")
            list_frame.pack(fill="both", expand=True)

            # Task list headers
            headers = ["Title", "Description", "Priority", "Deadline", "Duration (min)"]
            for i, header in enumerate(headers):
                tk.Label(
                    list_frame, text=header, font=("Helvetica", 12),
                    bg="#f0f2f5", fg="#34495e"
                ).grid(row=0, column=i, padx=5, pady=5, sticky="w")

            # Scrollbar for listboxes
            scroll = ttk.Scrollbar(list_frame, orient="vertical")
            scroll.grid(row=1, column=5, sticky="ns")

            # Task listboxes
            self.title_listbox = tk.Listbox(list_frame, width=20, height=15, font=("Helvetica", 11), yscrollcommand=scroll.set, selectmode=tk.SINGLE)
            self.description_listbox = tk.Listbox(list_frame, width=30, height=15, font=("Helvetica", 11), yscrollcommand=scroll.set, selectmode=tk.SINGLE)
            self.priority_listbox = tk.Listbox(list_frame, width=15, height=15, font=("Helvetica", 11), yscrollcommand=scroll.set, selectmode=tk.SINGLE)
            self.deadline_listbox = tk.Listbox(list_frame, width=25, height=15, font=("Helvetica", 11), yscrollcommand=scroll.set, selectmode=tk.SINGLE)
            self.duration_listbox = tk.Listbox(list_frame, width=15, height=15, font=("Helvetica", 11), yscrollcommand=scroll.set, selectmode=tk.SINGLE)

            self.title_listbox.grid(row=1, column=0, padx=5, pady=5)
            self.description_listbox.grid(row=1, column=1, padx=5, pady=5)
            self.priority_listbox.grid(row=1, column=2, padx=5, pady=5)
            self.deadline_listbox.grid(row=1, column=3, padx=5, pady=5)
            self.duration_listbox.grid(row=1, column=4, padx=5, pady=5)

            scroll.configure(command=self._sync_scroll)

            # Bind selection events
            for lb in [self.title_listbox, self.description_listbox, self.priority_listbox, self.deadline_listbox, self.duration_listbox]:
                lb.bind("<<ListboxSelect>>", self._sync_selection)
        except Exception as e:
            logger.exception(f"Error setting up MainWindow UI: {e}")
            raise

    def _sync_scroll(self, *args):
        """Synchronizes scrolling across listboxes."""
        try:
            for lb in [self.title_listbox, self.description_listbox, self.priority_listbox, self.deadline_listbox, self.duration_listbox]:
                lb.yview(*args)
        except Exception as e:
            logger.exception(f"Scroll sync error: {e}")

    def _sync_selection(self, event):
        """Synchronizes selection across listboxes."""
        if self.is_syncing_selection:
            return
        self.is_syncing_selection = True
        try:
            widget = event.widget
            selection = widget.curselection()
            for lb in [self.title_listbox, self.description_listbox, self.priority_listbox, self.deadline_listbox, self.duration_listbox]:
                lb.select_clear(0, tk.END)
                if selection:
                    lb.select_set(selection[0])
                    lb.see(selection[0])
            if selection and selection[0] < len(self.task_ids):
                self.selected_task_id = self.task_ids[selection[0]]
                self.selected_task_index = selection[0]
                logger.info(f"Selected task_id={self.selected_task_id}")
        except Exception as e:
            logger.exception(f"Selection sync error: {e}")
        finally:
            self.is_syncing_selection = False

    def _update_listboxes(self):
        """Refreshes listboxes with task data."""
        logger.info("Updating listboxes")
        try:
            self.title_listbox.delete(0, tk.END)
            self.description_listbox.delete(0, tk.END)
            self.priority_listbox.delete(0, tk.END)
            self.deadline_listbox.delete(0, tk.END)
            self.duration_listbox.delete(0, tk.END)
            self.task_ids = []

            tasks = self.task_manager.get_tasks(self.user_id, self.sort_var.get())
            logger.info(f"Fetched {len(tasks)} tasks for user_id={self.user_id}")
            if not isinstance(tasks, (list, tuple)):
                logger.error(f"Expected list of tasks, got {type(tasks)}: {tasks}")
                tasks = []
            for task in tasks:
                if not isinstance(task, (list, tuple)):
                    logger.error(f"Expected tuple for task, got {type(task)}: {task}")
                    continue
                task_id, title, description, priority, deadline_str, duration = task
                self.task_ids.append(task_id)
                self.title_listbox.insert(tk.END, title)
                self.description_listbox.insert(tk.END, description or "")
                self.priority_listbox.insert(tk.END, priority)
                self.deadline_listbox.insert(tk.END, deadline_str)
                self.duration_listbox.insert(tk.END, duration)
        except Exception as e:
            logger.exception(f"Error updating listboxes: {e}")
            tkMessageBox.showerror("Error", f"Failed to load tasks: {e}")

    def _open_add_task(self):
        """Opens form to add a new task."""
        logger.info("Opening add task form")
        try:
            TaskFormWindow(self, self.user_id, self.task_manager)
        except Exception as e:
            logger.exception(f"Error opening add task form: {e}")
            tkMessageBox.showerror("Error", f"Failed to open add task form: {e}")

    def _open_edit_task(self):
        """Opens form to edit selected task."""
        logger.info(f"Opening edit task form for task_id={self.selected_task_id}")
        try:
            self.task_manager.open_edit_task(self, self.user_id, self.selected_task_id)
        except Exception as e:
            logger.exception(f"Error opening edit task form: {e}")
            tkMessageBox.showerror("Error", f"Failed to open edit task form: {e}")

    def _delete_task(self):
        """Deletes selected task."""
        logger.info(f"Deleting task_id={self.selected_task_id}")
        try:
            self.task_manager.delete_task(self, self.user_id, self.selected_task_id)
            for lb in [self.title_listbox, self.description_listbox, self.priority_listbox, self.deadline_listbox, self.duration_listbox]:
                lb.select_clear(0, tk.END)
        except Exception as e:
            logger.exception(f"Error deleting task: {e}")
            tkMessageBox.showerror("Error", f"Failed to delete task: {e}")

    def _logout(self):
        """Logs out user and returns to login screen."""
        logger.info("Logging out")
        try:
            self.window.withdraw()  # Hide main window
            self.on_logout()
        except Exception as e:
            logger.exception(f"Logout error: {e}")
            raise

    def _check_deadline(self):
        """Checks for overdue or urgent tasks and shows alerts."""
        try:
            tasks = self.task_manager.get_tasks(self.user_id, sort_option="By Deadline")
            now = datetime.now()
            for task in tasks:
                task_id, title, description, priority, deadline_str, duration = task
                try:
                    deadline_dt = datetime.strptime(deadline_str, "%d/%m/%Y %I:%M %p")
                    time_left = (deadline_dt - now).total_seconds()
                    if time_left <= 0:
                        tkMessageBox.showerror("Overdue", f"{title} is overdue!")
                    elif time_left < 86400:  # 24 hours
                        tkMessageBox.showwarning("Urgent", f"{title} is due soon!")
                except ValueError:
                    logger.error(f"Invalid deadline format for task_id={task_id}: {deadline_str}")
        except Exception as e:
            logger.exception(f"Error checking deadlines: {e}")

    def _start_deadline_check(self):
        """Schedules periodic deadline checks."""
        self._check_deadline()
        self.window.after(60000, self._start_deadline_check)  # Check every 60 seconds

    def run(self):
        """Starts main window event loop."""
        logger.info("Starting MainWindow")
        try:
            self.window.update()
            self.window.mainloop()
        except Exception as e:
            logger.exception(f"MainWindow event loop error: {e}")
            raise