from database import Database


class Task:
    """
    A class representing a task in the task management system.

    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        description (str): A brief description of the task.
        db (Database): The database connection object.
    """

    def __init__(self, id=None, title=None, description=None, db=None):
        self.id = id
        self.title = title
        self.description = description
        self.db = db

    def _get_connection(self):
        if not hasattr(self.db, 'get_connection'):
            raise Exception("Database object must have a 'get_connection' method")
        return self.db.get_connection()

    @staticmethod
    def get_all(db=None):
        db = db or Database()
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return [Task(id=row[0], title=row[1], description=row[2], db=db) for row in rows]
        except Exception as e:
            raise Exception(f"Error fetching all tasks: {e}")

    @staticmethod
    def get_by_id(task_id, db=None):
        db = db or Database()
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(id=row[0], title=row[1], description=row[2], db=db)
            else:
                raise Exception("Task not found")
        except Exception as e:
            raise Exception(f"Error fetching task by ID: {e}")

    def save(self):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (self.title, self.description)
            )
            conn.commit()
            self.id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchval()
        except Exception as e:
            raise Exception(f"Error saving task: {e}")

    def update(self):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
                (self.title, self.description, self.id)
            )
            conn.commit()
        except Exception as e:
            raise Exception(f"Error updating task: {e}")

    @staticmethod
    def delete(task_id, db=None):
        db = db or Database()
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

            # صرفا جهت اینکه موقع تست دوباره از ID یک شروع کنه به ثبت کردن تسک جدید
            cursor.execute("DBCC CHECKIDENT ('tasks', RESEED, 0)")
            conn.commit()
        except Exception as e:
            raise Exception(f"Error deleting task: {e}")
