from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import pandas as pd
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('attendance.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        conn = get_db_connection()
        
        if role == 'student':
            user = conn.execute('SELECT * FROM students WHERE student_id = ? AND password = ?',
                               (username, password)).fetchone()
            if user:
                session['user_id'] = user['student_id']
                session['role'] = 'student'
                session['name'] = user['name']
                conn.close()
                return redirect(url_for('student_dashboard'))
        
        elif role == 'teacher':
            user = conn.execute('SELECT * FROM teachers WHERE teacher_id = ? AND password = ?',
                               (username, password)).fetchone()
            if user:
                session['user_id'] = user['teacher_id']
                session['role'] = 'teacher'
                session['name'] = user['name']
                conn.close()
                return redirect(url_for('teacher_dashboard'))
        
        elif role == 'club':
            user = conn.execute('SELECT * FROM clubs WHERE club_id = ? AND password = ?',
                               (username, password)).fetchone()
            if user:
                session['user_id'] = user['club_id']
                session['role'] = 'club'
                session['name'] = user['club_name']
                conn.close()
                return redirect(url_for('club_dashboard'))
        
        elif role == 'vc':
            user = conn.execute('SELECT * FROM vc WHERE vc_id = ? AND password = ?',
                               (username, password)).fetchone()
            if user:
                session['user_id'] = user['vc_id']
                session['role'] = 'vc'
                session['name'] = user['name']
                conn.close()
                return redirect(url_for('vc_dashboard'))
        
        conn.close()
        flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

# Student Dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student_id = session['user_id']
    
    # Get student info
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    
    # Get attendance records
    attendance = conn.execute('''
        SELECT a.*, t.name as teacher_name, t.subject 
        FROM attendance a 
        JOIN teachers t ON a.teacher_id = t.teacher_id 
        WHERE a.student_id = ? 
        ORDER BY a.date DESC, a.period DESC
    ''', (student_id,)).fetchall()
    
    # Calculate statistics
    total_classes = len(attendance)
    present = len([a for a in attendance if a['status'] == 'P'])
    absent = len([a for a in attendance if a['status'] == 'A'])
    not_marked = len([a for a in attendance if a['status'] == 'N.M.'])
    
    attendance_percentage = (present / total_classes * 100) if total_classes > 0 else 0
    
    conn.close()
    
    return render_template('student_dashboard.html', 
                          student=student,
                          attendance=attendance,
                          total_classes=total_classes,
                          present=present,
                          absent=absent,
                          not_marked=not_marked,
                          attendance_percentage=round(attendance_percentage, 2))

# Teacher Dashboard
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    teacher_id = session['user_id']
    
    # Get teacher info
    teacher = conn.execute('SELECT * FROM teachers WHERE teacher_id = ?', (teacher_id,)).fetchone()
    
    # Get all students
    students = conn.execute('SELECT * FROM students ORDER BY section, name').fetchall()
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get today's attendance for this teacher
    attendance_today = conn.execute('''
        SELECT a.*, s.name, s.section 
        FROM attendance a 
        JOIN students s ON a.student_id = s.student_id 
        WHERE a.teacher_id = ? AND a.date = ?
    ''', (teacher_id, today)).fetchall()
    
    conn.close()
    
    return render_template('teacher_dashboard.html',
                          teacher=teacher,
                          students=students,
                          attendance_today=attendance_today,
                          today=today)

# Mark Attendance
@app.route('/teacher/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    
    teacher_id = session['user_id']
    date = request.form['date']
    period = request.form['period']
    attendance_data = request.form.getlist('attendance[]')
    
    conn = get_db_connection()
    
    # Delete existing attendance for this teacher, date, and period
    conn.execute('DELETE FROM attendance WHERE teacher_id = ? AND date = ? AND period = ?',
                (teacher_id, date, period))
    
    # Insert new attendance records
    students = conn.execute('SELECT student_id FROM students').fetchall()
    
    for student in students:
        student_id = student['student_id']
        status = 'P' if student_id in attendance_data else 'A'
        
        conn.execute('''
            INSERT INTO attendance (student_id, teacher_id, date, period, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, teacher_id, date, period, status))
    
    conn.commit()
    conn.close()
    
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('teacher_dashboard'))

# Club Dashboard
@app.route('/club/dashboard')
def club_dashboard():
    if 'role' not in session or session['role'] != 'club':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    club_id = session['user_id']
    
    # Get club info
    club = conn.execute('SELECT * FROM clubs WHERE club_id = ?', (club_id,)).fetchone()
    
    # Get club events
    events = conn.execute('''
        SELECT * FROM club_events 
        WHERE club_id = ? 
        ORDER BY event_date DESC
    ''', (club_id,)).fetchall()
    
    # Get portal status
    portal_status = conn.execute('''
        SELECT * FROM portal_access 
        WHERE club_id = ? AND is_active = 1
    ''', (club_id,)).fetchone()
    
    conn.close()
    
    return render_template('club_dashboard.html',
                          club=club,
                          events=events,
                          portal_status=portal_status)

# Upload Excel File
@app.route('/club/upload', methods=['POST'])
def upload_excel():
    if 'role' not in session or session['role'] != 'club':
        return redirect(url_for('login'))
    
    club_id = session['user_id']
    
    # Check if portal is open for this club
    conn = get_db_connection()
    portal = conn.execute('''
        SELECT * FROM portal_access 
        WHERE club_id = ? AND is_active = 1
    ''', (club_id,)).fetchone()
    
    if not portal:
        conn.close()
        flash('Portal access is not active! Please contact VC.', 'error')
        return redirect(url_for('club_dashboard'))
    
    if 'excel_file' not in request.files:
        conn.close()
        flash('No file uploaded!', 'error')
        return redirect(url_for('club_dashboard'))
    
    file = request.files['excel_file']
    event_name = request.form['event_name']
    event_date = request.form['event_date']
    period = request.form['period']
    
    if file.filename == '':
        conn.close()
        flash('No file selected!', 'error')
        return redirect(url_for('club_dashboard'))
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read Excel file
            df = pd.read_excel(filepath)
            
            # Expected columns: Name, ID, Section, Year (adjust as needed)
            required_columns = ['Name', 'ID', 'Section', 'Year']
            
            # Create club event
            cursor = conn.execute('''
                INSERT INTO club_events (club_id, event_name, event_date, period, status)
                VALUES (?, ?, ?, ?, 'pending')
            ''', (club_id, event_name, event_date, period))
            event_id = cursor.lastrowid
            
            # Store student data for this event
            for _, row in df.iterrows():
                student_id = str(row['ID'])
                conn.execute('''
                    INSERT INTO event_attendance (event_id, student_id)
                    VALUES (?, ?)
                ''', (event_id, student_id))
            
            conn.commit()
            
            # Remove uploaded file
            os.remove(filepath)
            
            flash(f'Event "{event_name}" uploaded successfully! Waiting for VC approval.', 'success')
        
        except Exception as e:
            conn.rollback()
            flash(f'Error processing file: {str(e)}', 'error')
        
        finally:
            conn.close()
    else:
        conn.close()
        flash('Invalid file format! Please upload .xlsx or .xls file.', 'error')
    
    return redirect(url_for('club_dashboard'))

# VC Dashboard
@app.route('/vc/dashboard')
def vc_dashboard():
    if 'role' not in session or session['role'] != 'vc':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get all clubs
    clubs = conn.execute('SELECT * FROM clubs').fetchall()
    
    # Get pending events
    pending_events = conn.execute('''
        SELECT ce.*, c.club_name 
        FROM club_events ce 
        JOIN clubs c ON ce.club_id = c.club_id 
        WHERE ce.status = 'pending'
        ORDER BY ce.event_date DESC
    ''', ).fetchall()
    
    # Get portal access status
    portal_access = conn.execute('''
        SELECT pa.*, c.club_name 
        FROM portal_access pa 
        JOIN clubs c ON pa.club_id = c.club_id
        ORDER BY pa.is_active DESC, pa.opened_at DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('vc_dashboard.html',
                          clubs=clubs,
                          pending_events=pending_events,
                          portal_access=portal_access)

# Open Portal for Club
@app.route('/vc/open_portal', methods=['POST'])
def open_portal():
    if 'role' not in session or session['role'] != 'vc':
        return redirect(url_for('login'))
    
    club_id = request.form['club_id']
    duration_hours = int(request.form['duration_hours'])
    
    conn = get_db_connection()
    
    # Deactivate any existing active portals for this club
    conn.execute('UPDATE portal_access SET is_active = 0 WHERE club_id = ?', (club_id,))
    
    # Create new portal access
    conn.execute('''
        INSERT INTO portal_access (club_id, opened_by, duration_hours, is_active)
        VALUES (?, ?, ?, 1)
    ''', (club_id, session['user_id'], duration_hours))
    
    conn.commit()
    conn.close()
    
    flash('Portal opened successfully!', 'success')
    return redirect(url_for('vc_dashboard'))

# Close Portal for Club
@app.route('/vc/close_portal/<int:portal_id>', methods=['POST'])
def close_portal(portal_id):
    if 'role' not in session or session['role'] != 'vc':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('UPDATE portal_access SET is_active = 0 WHERE portal_id = ?', (portal_id,))
    conn.commit()
    conn.close()
    
    flash('Portal closed successfully!', 'success')
    return redirect(url_for('vc_dashboard'))

# Approve Event and Mark Attendance
@app.route('/vc/approve_event/<int:event_id>', methods=['POST'])
def approve_event(event_id):
    if 'role' not in session or session['role'] != 'vc':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get event details
    event = conn.execute('SELECT * FROM club_events WHERE event_id = ?', (event_id,)).fetchone()
    
    if not event:
        conn.close()
        flash('Event not found!', 'error')
        return redirect(url_for('vc_dashboard'))
    
    # Get students who attended this event
    event_students = conn.execute('''
        SELECT student_id FROM event_attendance WHERE event_id = ?
    ''', (event_id,)).fetchall()
    
    # Mark attendance as 'P' for these students
    # We need to find the teacher's class for this period and date
    # For simplicity, we'll mark it against a dummy teacher or system teacher
    # In real system, you'd match with actual teacher schedule
    
    teachers = conn.execute('SELECT teacher_id FROM teachers LIMIT 1').fetchone()
    if teachers:
        teacher_id = teachers['teacher_id']
        
        for student in event_students:
            student_id = student['student_id']
            
            # Check if attendance already exists
            existing = conn.execute('''
                SELECT * FROM attendance 
                WHERE student_id = ? AND date = ? AND period = ?
            ''', (student_id, event['event_date'], event['period'])).fetchone()
            
            if existing:
                # Update to Present
                conn.execute('''
                    UPDATE attendance 
                    SET status = 'P', marked_by_club = 1, club_event_id = ?
                    WHERE student_id = ? AND date = ? AND period = ?
                ''', (event_id, student_id, event['event_date'], event['period']))
            else:
                # Insert new attendance record
                conn.execute('''
                    INSERT INTO attendance (student_id, teacher_id, date, period, status, marked_by_club, club_event_id)
                    VALUES (?, ?, ?, ?, 'P', 1, ?)
                ''', (student_id, teacher_id, event['event_date'], event['period'], event_id))
    
    # Update event status
    conn.execute('UPDATE club_events SET status = "approved" WHERE event_id = ?', (event_id,))
    
    conn.commit()
    conn.close()
    
    flash('Event approved and attendance marked successfully!', 'success')
    return redirect(url_for('vc_dashboard'))

# Reject Event
@app.route('/vc/reject_event/<int:event_id>', methods=['POST'])
def reject_event(event_id):
    if 'role' not in session or session['role'] != 'vc':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('UPDATE club_events SET status = "rejected" WHERE event_id = ?', (event_id,))
    conn.commit()
    conn.close()
    
    flash('Event rejected!', 'success')
    return redirect(url_for('vc_dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)