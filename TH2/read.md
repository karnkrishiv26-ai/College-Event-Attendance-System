# AI-Based Attendance System - Club Event Integration

## 📋 Overview

This system automates attendance marking for club events in a college ERP. When students attend club events, their attendance is automatically marked for the classes they missed during that time.

## 🎯 Key Features

- **4 User Roles**: Student, Teacher, Club Leader, VC (Vice Chancellor)
- **Auto-Attendance Marking**: Upload Excel files from Google Forms to auto-mark attendance
- **VC Approval System**: VC controls which clubs can mark attendance and when
- **Real-time Dashboard**: Students can view their attendance instantly
- **Event Tracking**: All event-based attendance is tracked with event names

## 📁 File Structure

```
attendance_system/
├── app.py                          # Main Flask application
├── database.db                     # SQLite database (auto-created)
├── templates/
│   ├── login.html                  # Login page
│   ├── student_dashboard.html      # Student view
│   ├── teacher_portal.html         # Teacher attendance marking
│   ├── club_portal.html            # Club Excel upload
│   └── vc_portal.html              # VC control panel
├── static/
│   └── style.css                   # All styling
├── uploads/                        # Excel file uploads (auto-created)
└── README.md                       # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Required Packages

```bash
pip install flask pandas openpyxl
```

### Step 2: Create Directory Structure

```bash
mkdir attendance_system
cd attendance_system

# Create subdirectories
mkdir templates static uploads
```

### Step 3: Save All Files

Save the following files in their respective directories:
- `app.py` in root directory
- All `.html` files in `templates/` folder
- `style.css` in `static/` folder

### Step 4: Run the Application

```bash
python app.py
```

The application will start at: `http://127.0.0.1:5000/`

## 👥 Demo Credentials

### Students (20 available)
- **Username**: student1 to student20
- **Password**: pass123
- **Example**: student1 / pass123

### Teachers (4 available)
- **Username**: teacher1 to teacher4
- **Password**: pass123
- **Example**: teacher1 / pass123

### Club Leaders (2 available)
- **Username**: club1, club2
- **Password**: pass123
- **Clubs**: Tech Innovation Club, Coding Society

### Vice Chancellor
- **Username**: vc
- **Password**: pass123

## 📊 How It Works - Complete Workflow

### 1️⃣ **VC Approves Club** (VC Portal)
- Login as VC
- Navigate to "Registered Clubs"
- Approve clubs that want to use the system

### 2️⃣ **VC Creates Approval Window** (VC Portal)
- Select the approved club
- Enter event name (e.g., "Tech Hackathon 2025")
- Set start time and end time for when the club can upload attendance
- Click "Create Approval Window"

### 3️⃣ **Club Conducts Event**
- Club organizes event
- Students attend and fill Google Form with:
  - Name
  - Student ID
  - Section
  - Year

### 4️⃣ **Export to Excel**
- Google Forms automatically creates Excel file
- Download the Excel file

### 5️⃣ **Club Uploads Attendance** (Club Portal)
- Login as club leader
- Check "Active Approval Windows"
- Upload the Excel file
- System automatically:
  - Reads student IDs
  - Finds classes marked as "N.M." (Not Mentioned) for that day
  - Changes status to "P" (Present)
  - Adds event name for tracking

### 6️⃣ **Students View Updated Attendance** (Student Dashboard)
- Login as student
- View today's attendance
- See which classes were marked due to events

## 📄 Excel File Format

Your Excel file from Google Forms should have these columns:

| Name | Student ID | Section | Year |
|------|------------|---------|------|
| Krishiv Karn | 25030175 | Section-J | 1 |
| Rahul Sharma | 25030176 | Section-J | 1 |
| Priya Singh | 25030177 | Section-J | 1 |

**Important**: 
- Column names must match exactly
- Student ID is the key field for matching
- Google Forms automatically creates this format

## 🎨 Portal Features

### Student Dashboard
- View attendance percentage
- See today's class-wise attendance
- Check which classes were marked due to events
- View personal information

### Teacher Portal
- Mark manual attendance for classes
- Select subject, period, and date
- Mark students as P (Present), A (Absent), or N.M. (Not Mentioned)
- View assigned subjects

### Club Portal
- View club information and status
- See active approval windows
- Upload Excel files during approved time windows
- View approval history
- See Excel format guide

### VC Portal
- View attendance statistics
- Approve/manage clubs
- Create approval windows for events
- Revoke approvals if needed
- Monitor all event-based attendance

## 🔧 Technical Details

### Database Schema

**Users Table**
- Stores all users (students, teachers, club leaders, VC)
- Fields: username, password, role, name, student_id, section, year

**Clubs Table**
- Registered clubs
- Fields: club_name, leader_username, status

**VC Approvals Table**
- Time windows for club uploads
- Fields: club_id, event_name, start_time, end_time, status

**Subjects Table**
- Course information
- Fields: subject_code, subject_name, teacher_username

**Attendance Table**
- All attendance records
- Fields: student_id, subject_code, date, period, status, marked_by, event_name

### Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS
- **File Processing**: pandas, openpyxl

## 🧪 Testing the System

### Test Scenario 1: Manual Attendance
1. Login as `teacher1` / `pass123`
2. Select a subject
3. Choose period and today's date
4. Mark attendance for students
5. Login as `student1` / `pass123` to verify

### Test Scenario 2: Event-Based Attendance
1. Login as `vc` / `pass123`
2. Approve a club if not already approved
3. Create approval window (set start time to current time, end time to 2 hours later)
4. Login as `club1` / `pass123`
5. Create a sample Excel file with student IDs: 25030175, 25030176, 25030177
6. Upload the Excel file
7. Login as students to see updated attendance

### Test Scenario 3: VC Controls
1. Login as `vc` / `pass123`
2. View attendance statistics
3. Create multiple approval windows
4. Revoke an approval
5. Check that revoked approvals can't be used

## 🔐 Security Considerations

**Note**: This is a prototype for demonstration purposes. For production use:
- Implement proper password hashing (bcrypt)
- Add CSRF protection
- Use environment variables for secret keys
- Implement proper session management
- Add input validation and sanitization
- Use HTTPS
- Implement rate limiting
- Add role-based access control middleware

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete database and restart to reset
rm database.db
python app.py
```

### Excel Upload Fails
- Check file format (.xlsx or .xls)
- Verify column names match exactly
- Ensure Student IDs exist in database
- Check if approval window is active

### Port Already in Use
```python
# In app.py, change the port:
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

## 📝 Sample Data Included

### 20 Students
- IDs: 25030175 to 25030194
- Sections: Section-J and Section-K
- Year: 1 (First Year)

### 4 Teachers
- Soham Bhandari (teacher1)
- Mohit Kumar (teacher2)
- Sunita Danu (teacher3)
- Manvi Walia (teacher4)

### 4 Subjects
- Technical Training - Advance Programming in C
- Environmental Studies-I
- HTML5 and CSS Lab
- Basics of Computer and C Programming

### 2 Clubs
- Tech Innovation Club
- Coding Society

## 🎯 Future Enhancements

- Email notifications for attendance updates
- SMS integration for low attendance alerts
- Analytics dashboard with charts
- Export attendance reports to PDF/Excel
- Multi-semester support
- Biometric integration
- Mobile app
- Real-time notifications

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the workflow diagram
3. Test with demo credentials
4. Check console logs for errors

## 📜 License

This is a prototype for educational purposes.

---

**Built with ❤️ for Quantum University**

**Version**: 1.0  
**Last Updated**: 2025