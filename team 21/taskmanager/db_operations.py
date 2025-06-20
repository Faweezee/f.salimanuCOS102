import psycopg2

class Database:
    """Handles PostgreSQL database operations."""
    def __init__(self):
        self.conn = None

    def connect(self):
        """Connects to the db"""
        try:
            self.conn = psycopg2.connect(
                dbname='task_manager_db',
                user='postgres',
                password='cos101',
                host='localhost',
                port='5432'
            )
            return True
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            return False

    def close(self):
        """Closes database connection."""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Creates users and tasks tables if they don't exist."""
        if not self.connect():
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        priority VARCHAR(10) NOT NULL,
                        deadline_str VARCHAR(50) NOT NULL,
                        deadline_datetime TIMESTAMP NOT NULL,
                        duration INTEGER NOT NULL,
                        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
                    );
                """)
                self.conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Failed to create tables: {e}")
            return False
        finally:
            self.close()

    def insert_user(self, username, password):
        """Inserts a new user into the database."""
        if not self.connect():
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
                    (username, password)
                )
                user_id = cur.fetchone()[0]
                self.conn.commit()
                print(f"Registered user_id={user_id}")
                return user_id
        except psycopg2.Error as e:
            print(f"User creation failed: {e}")
            return None
        finally:
            self.close()

    def authenticate_user(self, username, password):
        """Authenticates a user by username and password."""
        if not self.connect():
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM users WHERE username = %s AND password = %s;",
                    (username, password)
                )
                result = cur.fetchone()
                user_id = result[0] if result else None
                print(f"Authenticated user_id={user_id}")
                return user_id
        except psycopg2.Error as e:
            print(f"Authentication failed: {e}")
            return None
        finally:
            self.close()

    def insert_task(self, title, description, priority, deadline_str, deadline_datetime, duration, user_id):
        """Inserts a new task into the database."""
        if not self.connect():
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO tasks (title, description, priority, deadline_str, deadline_datetime, duration, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                """, (title, description, priority, deadline_str, deadline_datetime, duration, user_id))
                task_id = cur.fetchone()[0]
                self.conn.commit()
                print(f"Inserted task_id={task_id} for user_id={user_id}")
                return task_id
        except psycopg2.Error as e:
            print(f"Insert task failed: {e}")
            return None
        finally:
            self.close()

    def update_task(self, task_id, title, description, priority, deadline_str, deadline_datetime, duration, user_id):
        """Updates an existing task in the database."""
        if not self.connect():
            return False
        try:
            with self.conn.cursor() as cur:
                print(f"Attempting to update task_id={task_id} for user_id={user_id}")
                cur.execute("""
                    UPDATE tasks
                    SET title = %s, description = %s, priority = %s, deadline_str = %s,
                        deadline_datetime = %s, duration = %s
                    WHERE id = %s AND user_id = %s;
                """, (title, description, priority, deadline_str, deadline_datetime, duration, task_id, user_id))
                success = cur.rowcount > 0
                self.conn.commit()
                if success:
                    print(f"Successfully updated task_id={task_id}")
                else:
                    print(f"No task found with task_id={task_id} for user_id={user_id}")
                return success
        except psycopg2.Error as e:
            print(f"Update task failed: {e}")
            return False
        finally:
            self.close()

    def delete_task(self, task_id, user_id):
        """Deletes a task from the database."""
        if not self.connect():
            return False
        try:
            with self.conn.cursor() as cur:
                print(f"Attempting to delete task_id={task_id} for user_id={user_id}")
                
                # Check if the task exists for the user
                cur.execute("SELECT id FROM tasks WHERE id = %s AND user_id = %s;", (task_id, user_id))
                if not cur.fetchone():
                    print(f"No task found with task_id={task_id} for user_id={user_id}")
                    return False
                
                cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s;", (task_id, user_id))
                self.conn.commit()
                print(f"Successfully deleted task_id={task_id}")
                return True
        except psycopg2.Error as e:
            print(f"Delete task failed: {e}")
            return False
        finally:
            self.close()

    def fetch_tasks(self, user_id, sort_option="By Deadline"):
        """Fetches all tasks for a user with sorting."""
        if not self.connect():
            return []
        try:
            with self.conn.cursor() as cur:
                if sort_option == "By Priority":
                    cur.execute("""
                        SELECT id, title, description, priority, deadline_str, duration
                        FROM tasks
                        WHERE user_id = %s
                        ORDER BY
                            CASE priority
                                WHEN 'High' THEN 1
                                WHEN 'Medium' THEN 2
                                WHEN 'Low' THEN 3
                            END,
                            deadline_datetime;
                    """, (user_id,))
                else:  # By Deadline
                    cur.execute(
                        "SELECT id, title, description, priority, deadline_str, duration FROM tasks WHERE user_id = %s ORDER BY deadline_datetime;",
                        (user_id,)
                    )
                tasks = cur.fetchall()
                print(f"Fetched tasks for user_id={user_id}: {tasks}")
                return tasks
        except psycopg2.Error as e:
            print(f"Fetch tasks failed: {e}")
            return []
        finally:
            self.close()