import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "attendance.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Initializing database...")

    # ========================
    #  TABLE CREATIONS
    # ========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            section TEXT NOT NULL,
            year INTEGER NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clubs (
            club_id TEXT PRIMARY KEY,
            club_name TEXT NOT NULL,
            password TEXT NOT NULL,
            is_registered INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vc (
            vc_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            teacher_id TEXT NOT NULL,
            date TEXT NOT NULL,
            period INTEGER NOT NULL,
            status TEXT NOT NULL,
            marked_by_club INTEGER DEFAULT 0,
            club_event_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS club_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id TEXT NOT NULL,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            period INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (club_id) REFERENCES clubs(club_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_attendance (
            event_attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES club_events(event_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portal_access (
            portal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id TEXT NOT NULL,
            opened_by TEXT NOT NULL,
            opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_hours INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (club_id) REFERENCES clubs(club_id),
            FOREIGN KEY (opened_by) REFERENCES vc(vc_id)
        )
    """)

    # ========================
    #  INSERT SAMPLE DATA
    # ========================

    # ---- Students ----
    students = [
        ('2021001', 'Rahul Kumar', 'A', 3, 'pass123'),
        ('2021002', 'Priya Sharma', 'A', 3, 'pass123'),
        ('2021003', 'Amit Singh', 'A', 3, 'pass123'),
        ('2021004', 'Sneha Gupta', 'B', 3, 'pass123'),
        ('2021005', 'Rohan Verma', 'B', 3, 'pass123'),
        ('2021006', 'Anjali Patel', 'B', 3, 'pass123'),
        ('2021007', 'Vijay Kumar', 'C', 3, 'pass123'),
        ('2021008', 'Neha Singh', 'C', 3, 'pass123'),
        ('2021009', 'Karan Mehta', 'C', 3, 'pass123'),
        ('2021010', 'Pooja Reddy', 'A', 3, 'pass123'),
        ('2021011', 'Arjun Nair', 'A', 3, 'pass123'),
        ('2021012', 'Divya Joshi', 'B', 3, 'pass123'),
        ('2021013', 'Suresh Yadav', 'B', 3, 'pass123'),
        ('2021014', 'Kavita Das', 'C', 3, 'pass123'),
        ('2021015', 'Manish Pandey', 'C', 3, 'pass123'),
        ('2021016', 'Aarti Mishra', 'A', 3, 'pass123'),
        ('2021017', 'Deepak Sinha', 'A', 3, 'pass123'),
        ('2021018', 'Ritu Agarwal', 'B', 3, 'pass123'),
        ('2021019', 'Sanjay Iyer', 'B', 3, 'pass123'),
        ('2021020', 'Meera Saxena', 'C', 3, 'pass123'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO students (student_id, name, section, year, password)
        VALUES (?, ?, ?, ?, ?)
    """, students)

    # ---- Teachers ----
    teachers = [
        ('T001', 'Dr. Rajesh Kumar', 'Data Structures', 'teach123'),
        ('T002', 'Prof. Sunita Verma', 'Database Management', 'teach123'),
        ('T003', 'Dr. Anil Sharma', 'Computer Networks', 'teach123'),
        ('T004', 'Prof. Meena Gupta', 'Operating Systems', 'teach123'),
        ('T005', 'Dr. Prakash Singh', 'Web Technology', 'teach123'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO teachers (teacher_id, name, subject, password)
        VALUES (?, ?, ?, ?)
    """, teachers)

    # ---- Clubs ----
    clubs = [
        ('CLUB001', 'Coding Club', 'club123'),
        ('CLUB002', 'Tech Fest Committee', 'club123'),
        ('CLUB003', 'Robotics Club', 'club123'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO clubs (club_id, club_name, password)
        VALUES (?, ?, ?)
    """, clubs)

    # ---- VC ----
    cursor.execute("""
        INSERT OR IGNORE INTO vc (vc_id, name, password)
        VALUES ('VC001', 'Dr. Vice Chancellor', 'vc123')
    """)

    # ---- Generate 10 Days of Attendance ----
    statuses = ['P', 'A', 'N.M.']
    today = datetime.now()

    for i in range(10):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        for period in range(1, 6):
            teacher_id = random.choice(['T001', 'T002', 'T003', 'T004', 'T005'])
            for student in students:
                student_id = student[0]
                status = random.choices(statuses, weights=[70, 20, 10])[0]

                cursor.execute("""
                    INSERT OR IGNORE INTO attendance (student_id, teacher_id, date, period, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (student_id, teacher_id, date, period, status))

    conn.commit()
    conn.close()

    print("\nDatabase initialized successfully!")
    print("\n===== LOGIN CREDENTIALS =====")
    print("Student: 2021001 / pass123")
    print("Teacher: T001 / teach123")
    print("Club   : CLUB001 / club123")
    print("VC     : VC001 / vc123")
    print("=============================\n")


if __name__ == "__main__":
    init_database()