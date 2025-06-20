import tkinter as tk
from gui import LoginWindow, MainWindow
import logging

# Configure logging
# Set to INFO for production; change to DEBUG for detailed debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    """Entry point for the task manager application."""
    logger.info("Starting application")
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        def on_logout():
            """Callback for logout, restarts login window."""
            logger.info("User logged out")
            login_window = LoginWindow(root, on_success)
            login_window.run()

        def on_success(user_id):
            """Callback for successful login/register."""
            logger.info(f"Login success for user_id={user_id}")
            main_window = MainWindow(root, user_id, on_logout)
            main_window.run()

        login_window = LoginWindow(root, on_success)
        login_window.run()
        try:
            root.destroy()
        except tk.TclError:
            logger.info("Root already destroyed")
        logger.info("Application exited")
    except Exception as e:
        logger.exception(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()