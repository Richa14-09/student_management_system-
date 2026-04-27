import sqlite3
from datetime import datetime

class StudentDatabase:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to {self.db_name}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def create_table(self):
        """Create students table if not exists"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            print("Table created successfully")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
    
    def add_student(self, roll_no, name, email, phone, age, grade, address):
        """Add new student"""
        try:
            self.cursor.execute('''
                INSERT INTO students 
                (roll_no, name, email, phone, age, grade, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (roll_no, name, email, phone, age, grade, address))
            self.conn.commit()
            return True, "Student added successfully"
        except sqlite3.IntegrityError:
            return False, "Roll number already exists"
        except sqlite3.Error as e:
            return False, f"Error: {e}"
    
    def get_all_students(self):
        """Retrieve all students"""
        try:
            self.cursor.execute('SELECT * FROM students')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return []
    
    def search_student(self, search_term):
        """Search student by roll_no or name"""
        try:
            self.cursor.execute('''
                SELECT * FROM students 
                WHERE roll_no LIKE ? OR name LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return []
    
    def update_student(self, id, roll_no, name, email, phone, age, grade, address):
        """Update student record"""
        try:
            self.cursor.execute('''
                UPDATE students 
                SET roll_no=?, name=?, email=?, phone=?, age=?, grade=?, address=?
                WHERE id=?
            ''', (roll_no, name, email, phone, age, grade, address, id))
            self.conn.commit()
            return True, "Student updated successfully"
        except sqlite3.Error as e:
            return False, f"Error: {e}"
    
    def delete_student(self, id):
        """Delete student record"""
        try:
            self.cursor.execute('DELETE FROM students WHERE id=?', (id,))
            self.conn.commit()
            return True, "Student deleted successfully"
        except sqlite3.Error as e:
            return False, f"Error: {e}"
    
    def get_student_by_id(self, id):
        """Get student by ID"""
        try:
            self.cursor.execute('SELECT * FROM students WHERE id=?', (id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()