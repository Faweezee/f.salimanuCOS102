class Task:
    def __init__(self, title, priority, deadline_datetime, deadline_str, duration, description, user_id):
        # Initialize task attributes
        self.title = title
        self.priority = priority
        self.deadline_datetime = deadline_datetime
        self.deadline_str = deadline_str
        self.duration = duration
        self.description = description
        self.user_id = user_id