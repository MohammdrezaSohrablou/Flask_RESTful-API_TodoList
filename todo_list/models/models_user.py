class User:
    def __init__(self, id=None, username=None, password_hash=None, email=None, phone=None, db=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.phone = phone
        self.db = db

    @staticmethod
    def find_by_username(username, db):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, email, phone FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return User(id=row[0], username=row[1], password_hash=row[2], email=row[3], phone=row[4], db=db)

    def save(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, phone) VALUES (?, ?, ?, ?)",
            (self.username, self.password_hash, self.email, self.phone)
        )
        conn.commit()
        self.id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchval()
