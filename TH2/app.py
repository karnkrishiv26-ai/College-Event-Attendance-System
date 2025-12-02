# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
import pandas as pd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'database.db')

ALLOWED_EXT = {'xlsx', 'xls', 'csv'}

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-change-me')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024  # 6 MB limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------- DB helpers ----------
def get_db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables and seed demo data (idempotent)."""
    conn = get_db_conn()
    c = conn.cursor()
    # Tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        name TEXT,
        student_id TEXT,
        section TEXT,
        year INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS clubs (
        id INTEGER PRIMARY KEY,
        club_name TEXT UNIQUE,
        leader_username TEXT,
        status TEXT DEFAULT 'pending'
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS vc_approvals (
        id INTEGER PRIMARY KEY,
        club_id INTEGER,
        event_name TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(club_id) REFERENCES clubs(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        subject_code TEXT,
        subject_name TEXT,
        teacher_username TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        student_id TEXT,
        subject_code TEXT,
        date TEXT,
        period TEXT,
        status TEXT,
        marked_by TEXT,
        event_name TEXT
    )''')

    # seed users (20 students)
    students = [
        ('student1','pass123','student','Krishiv Karn','25030175','Section-J',1),
        ('student2','pass123','student','Rahul Sharma','25030176','Section-J',1),
        ('student3','pass123','student','Priya Singh','25030177','Section-J',1),
        ('student4','pass123','student','Amit Kumar','25030178','Section-K',1),
        ('student5','pass123','student','Neha Gupta','25030179','Section-K',1),
        ('student6','pass123','student','Rohan Verma','25030180','Section-J',1),
        ('student7','pass123','student','Anjali Patel','25030181','Section-J',1),
        ('student8','pass123','student','Vikram Reddy','25030182','Section-K',1),
        ('student9','pass123','student','Sneha Desai','25030183','Section-K',1),
        ('student10','pass123','student','Arjun Mehta','25030184','Section-J',1),
        ('student11','pass123','student','Pooja Joshi','25030185','Section-J',1),
        ('student12','pass123','student','Karan Nair','25030186','Section-K',1),
        ('student13','pass123','student','Divya Iyer','25030187','Section-K',1),
        ('student14','pass123','student','Siddharth Rao','25030188','Section-J',1),
        ('student15','pass123','student','Kavya Pillai','25030189','Section-J',1),
        ('student16','pass123','student','Aditya Shah','25030190','Section-K',1),
        ('student17','pass123','student','Riya Kapoor','25030191','Section-K',1),
        ('student18','pass123','student','Varun Sinha','25030192','Section-J',1),
        ('student19','pass123','student','Tanvi Agarwal','25030193','Section-J',1),
        ('student20','pass123','student','Harsh Bansal','25030194','Section-K',1),
    ]
    for u in students:
        username, pw, role, name, studid, section, year = u
        hashed = generate_password_hash(pw)
        try:
            c.execute('INSERT INTO users (username,password,role,name,student_id,section,year) VALUES (?,?,?,?,?,?,?)',
                      (username, hashed, role, name, studid, section, year))
        except sqlite3.IntegrityError:
            pass

    # teachers
    teachers = [
        ('teacher1','pass123','teacher','Soham Bhandari', None, None, None),
        ('teacher2','pass123','teacher','Mohit Kumar', None, None, None),
        ('teacher3','pass123','teacher','Sunita Danu', None, None, None),
        ('teacher4','pass123','teacher','Manvi Walia', None, None, None),
    ]
    for u in teachers:
        username, pw, role, name, *_ = u
        hashed = generate_password_hash(pw)
        try:
            c.execute('INSERT INTO users (username,password,role,name) VALUES (?,?,?,?)',
                      (username, hashed, role, name))
        except sqlite3.IntegrityError:
            pass

    # club leaders
    clubs_users = [
        ('club1','pass123','club','Tech Club Leader', None, None, None),
        ('club2','pass123','club','Coding Club Leader', None, None, None),
    ]
    for u in clubs_users:
        username, pw, role, name, *_ = u
        hashed = generate_password_hash(pw)
        try:
            c.execute('INSERT INTO users (username,password,role,name) VALUES (?,?,?,?)',
                      (username, hashed, role, name))
        except sqlite3.IntegrityError:
            pass

    # vc
    try:
        c.execute('INSERT INTO users (username,password,role,name) VALUES (?,?,?,?)',
                  ('vc', generate_password_hash('pass123'), 'vc', 'Vice Chancellor'))
    except sqlite3.IntegrityError:
        pass

    # clubs table
    clubs = [
        ('Tech Innovation Club','club1','approved'),
        ('Coding Society','club2','approved'),
    ]
    for cl in clubs:
        try:
            c.execute('INSERT INTO clubs (club_name, leader_username, status) VALUES (?,?,?)', cl)
        except sqlite3.IntegrityError:
            pass

    # subjects
    subjects = [
        ('SE31164','Technical Training - Advance Programming in C','teacher1'),
        ('VC31103','Environmental Studies-I','teacher2'),
        ('CS32166','HTML5 and CSS Lab','teacher4'),
        ('CS31101','Basics of Computer and C Programming','teacher3'),
    ]
    for s in subjects:
        try:
            c.execute('INSERT INTO subjects (subject_code, subject_name, teacher_username) VALUES (?,?,?)', s)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# initialize DB once
init_db()


# ---------- Utilities ----------
def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXT

def read_uploaded_file(path):
    """Return list of student_id strings read from uploaded Excel/CSV."""
    ext = path.rsplit('.', 1)[1].lower()
    if ext in ('xls','xlsx'):
        df = pd.read_excel(path, engine='openpyxl')
    else:
        df = pd.read_csv(path)
    # normalize column name possibilities
    cols = [c.strip().lower() for c in df.columns]
    sid_col = None
    for candidate in ['student id', 'student_id', 'id', 'roll no', 'roll']:
        if candidate in cols:
            sid_col = df.columns[cols.index(candidate)]
            break
    if not sid_col:
        raise ValueError('No Student ID column found (expected "Student ID").')
    student_ids = df[sid_col].astype(str).str.strip().tolist()
    return student_ids


# ---------- Routes ----------
@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=?', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user['name']
            session.permanent = True
            if user['role'] == 'student':
                session['student_id'] = user['student_id']
                return redirect(url_for('student_dashboard'))
            if user['role'] == 'teacher':
                return redirect(url_for('teacher_portal'))
            if user['role'] == 'club':
                return redirect(url_for('club_portal'))
            if user['role'] == 'vc':
                return redirect(url_for('vc_portal'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------- Student ----------
@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    student_id = session.get('student_id')
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE student_id=?', (student_id,))
    student = c.fetchone()
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('''SELECT s.subject_name, a.subject_code, a.period, a.status, a.marked_by, a.event_name
                 FROM attendance a LEFT JOIN subjects s ON a.subject_code = s.subject_code
                 WHERE a.student_id=? AND a.date=? ORDER BY a.period''', (student_id, today))
    today_attendance = c.fetchall()
    # simple percent across all attendance rows
    c.execute('SELECT COUNT(*) FROM attendance WHERE student_id=? AND status="P"', (student_id,))
    present = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM attendance WHERE student_id=? AND status IN ("P","A")', (student_id,))
    total = c.fetchone()[0]
    percent = round((present/total*100) if total>0 else 0,2)
    conn.close()
    return render_template('student_dashboard.html', student=student, today_attendance=today_attendance, attendance_percent=percent)

# ---------- Teacher ----------
@app.route('/teacher_portal', methods=['GET','POST'])
def teacher_portal():
    if 'username' not in session or session.get('role') != 'teacher':
        return redirect(url_for('login'))
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM subjects WHERE teacher_username=?', (session['username'],))
    subjects = c.fetchall()
    if request.method == 'POST':
        subject_code = request.form.get('subject_code')
        period = request.form.get('period')
        date = request.form.get('date')
        # all students
        c.execute('SELECT student_id, name, section FROM users WHERE role="student" ORDER BY section, name')
        students = c.fetchall()
        for s in students:
            sid = s['student_id']
            status = request.form.get(f'attendance_{sid}', 'N.M.')
            # check existing
            c.execute('SELECT id FROM attendance WHERE student_id=? AND subject_code=? AND date=? AND period=?',
                      (sid, subject_code, date, period))
            existing = c.fetchone()
            if existing:
                c.execute('UPDATE attendance SET status=?, marked_by=? WHERE id=?', (status, session['username'], existing['id']))
            else:
                c.execute('INSERT INTO attendance (student_id,subject_code,date,period,status,marked_by) VALUES (?,?,?,?,?,?)',
                          (sid, subject_code, date, period, status, session['username']))
        conn.commit()
        flash('Attendance saved!', 'success')
    c.execute('SELECT student_id, name, section FROM users WHERE role="student" ORDER BY section, name')
    students = c.fetchall()
    conn.close()
    return render_template('teacher_portal.html', subjects=subjects, students=students)

# ---------- Club ----------
@app.route('/club_portal', methods=['GET','POST'])
def club_portal():
    if 'username' not in session or session.get('role') != 'club':
        return redirect(url_for('login'))
    conn = get_db_conn()
    c = conn.cursor()
    # find club for this leader
    c.execute('SELECT * FROM clubs WHERE leader_username=?', (session['username'],))
    club = c.fetchone()
    if not club:
        flash('No club assigned to this account', 'danger')
        conn.close()
        return render_template('club_portal.html', club=None, approvals=[], active_approvals=[])
    club_id = club['id']
    # approvals for this club
    now_iso = datetime.utcnow().isoformat()
    c.execute('''SELECT * FROM vc_approvals WHERE club_id=? ORDER BY id DESC''', (club_id,))
    approvals = c.fetchall()
    # active approvals (approved & within window)
    c.execute('''SELECT * FROM vc_approvals WHERE club_id=? AND status='approved' 
                 AND start_time <= ? AND end_time >= ?''', (club_id, now_iso, now_iso))
    active = c.fetchall()

    if request.method == 'POST':
        file = request.files.get('file')
        approval_id = request.form.get('approval_id')
        event_name = request.form.get('event_name', 'Event')
        period = request.form.get('period', 'Event')
        if not file or file.filename == '':
            flash('No file uploaded', 'danger')
        elif not allowed_file(file.filename):
            flash('Invalid file type', 'danger')
        else:
            # ensure approval still active
            c.execute('SELECT * FROM vc_approvals WHERE id=? AND status="approved" AND start_time<=? AND end_time>=?',
                      (approval_id, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))
            ok = c.fetchone()
            if not ok:
                flash('Approval window is not active or valid', 'danger')
            else:
                filename = secure_filename(file.filename)
                ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                save_name = f"{ts}_{filename}"
                path = os.path.join(app.config['UPLOAD_FOLDER'], save_name)
                file.save(path)
                try:
                    student_ids = read_uploaded_file(path)
                    # mark attendance: convert N.M. -> P for today's entries
                    today = datetime.utcnow().strftime('%Y-%m-%d')
                    marked = 0
                    for sid in student_ids:
                        # find records for today with N.M.
                        c.execute('SELECT id, subject_code FROM attendance WHERE student_id=? AND date=? AND status IN ("N.M.","pending")', (sid, today))
                        rows = c.fetchall()
                        if not rows:
                            # optionally create an Event-period attendance entry (if they have no classes marked)
                            continue
                        for r in rows:
                            c.execute('UPDATE attendance SET status="P", marked_by=?, event_name=? WHERE id=?',
                                      (session['username'], event_name, r['id']))
                            marked += 1
                    conn.commit()
                    flash(f'Processed file, marked {marked} entries', 'success')
                except Exception as e:
                    flash(f'Error processing file: {str(e)}', 'danger')
                finally:
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    conn.close()
    return render_template('club_portal.html', club=club, approvals=approvals, active_approvals=active)

# ---------- VC ----------
@app.route('/vc_portal', methods=['GET','POST'])
def vc_portal():
    if 'username' not in session or session.get('role') != 'vc':
        return redirect(url_for('login'))
    conn = get_db_conn()
    c = conn.cursor()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'approve_club':
            club_id = request.form.get('club_id')
            c.execute('UPDATE clubs SET status="approved" WHERE id=?', (club_id,))
            conn.commit()
            flash('Club approved', 'success')
        elif action == 'create_approval':
            club_id = request.form.get('club_id')
            event_name = request.form.get('event_name')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            # store as ISO strings (UTC)
            try:
                st = datetime.fromisoformat(start_time).astimezone().isoformat()
                et = datetime.fromisoformat(end_time).astimezone().isoformat()
            except Exception:
                # if naive datetime (no tz), store as-is in isoformat
                st = datetime.fromisoformat(start_time).isoformat()
                et = datetime.fromisoformat(end_time).isoformat()
            c.execute('INSERT INTO vc_approvals (club_id,event_name,start_time,end_time,status) VALUES (?,?,?,?,?)',
                      (club_id, event_name, st, et, 'approved'))
            conn.commit()
            flash('Approval window created', 'success')
        elif action == 'revoke_approval':
            approval_id = request.form.get('approval_id')
            c.execute('UPDATE vc_approvals SET status="revoked" WHERE id=?', (approval_id,))
            conn.commit()
            flash('Approval revoked', 'success')

    # queries
    c.execute('SELECT * FROM clubs')
    clubs = c.fetchall()
    c.execute('''SELECT va.*, c.club_name FROM vc_approvals va JOIN clubs c ON va.club_id=c.id ORDER BY va.id DESC''')
    approvals = c.fetchall()
    c.execute('SELECT COUNT(*) FROM attendance WHERE status="P"')
    total_present = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM attendance WHERE status="A"')
    total_absent = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM attendance WHERE event_name IS NOT NULL')
    event_marked = c.fetchone()[0]
    conn.close()
    stats = {'present': total_present, 'absent': total_absent, 'event_marked': event_marked}
    return render_template('vc_portal.html', clubs=clubs, approvals=approvals, stats=stats)

# static file route (optional)
@app.route('/uploads/<path:filename>')
def uploads_serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # run on localhost for dev
    app.run(debug=True, host='127.0.0.1', port=5000)
