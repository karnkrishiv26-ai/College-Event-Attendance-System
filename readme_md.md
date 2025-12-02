# AI-Based Attendance System with Club Event Integration

## Overview
This system allows clubs to upload attendance data from Google Forms (Excel format), which is then reviewed by the Vice Chancellor and automatically marked in the college ERP system.

## System Flow
```
Club Leader → Upload Excel → VC Approval → Automatic Attendance Marking → Student View
```

## Features
- **4 User Roles**: Student, Teacher, Club Leader, VC
- **Portal Access Control**: VC can open/close portal for specific clubs
- **Excel Upload**: Clubs upload Google Form responses as Excel files
- **Approval Workflow**: VC reviews and approves/rejects event attendance
- **Automatic Marking**: Approved attendance is automatically marked in the system
- **Student Dashboard**: Students can view their attendance with club event indicators

## File Structure
```
project/
│
├── app.py                          # Main Flask application
├── database.py                     # Database initialization script
├── requirements.txt                # Python dependencies
├── attendance.db                   # SQLite database (created on first run)
│
├── templates/                      # HTML templates
│   ├── login.html
│   ├── student_dashboard.html
│   ├── teacher_dashboard.html
│   ├── club_dashboard.html
│   └── vc_dashboard.html
│
├── static/                         # Static files
│   └── style.css
│
└── uploads/                        # Temporary Excel file storage
```

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python database.py
```

This will create `attendance.db` with sample data for 20 students, 5 teachers, 3 clubs, and 1 VC.

### 3. Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Login Credentials

### Student Access
- **Username**: 2021001 to 2021020 (any student ID)
- **Password**: pass123
- **Features**: View attendance, see statistics, identify club event attendance

### Teacher Access
- **Username**: T001, T002, T003, T004, or T005
- **Password**: teach123
- **Features**: Mark attendance for classes, view today's attendance

### Club Leader Access
- **Username**: CLUB001, CLUB002, or CLUB003
- **Password**: club123
- **Features**: 
  - Upload Excel files (when portal is open)
  - View event history
  - Check portal status

### Vice Chancellor Access
- **Username**: VC001
- **Password**: vc123
- **Features**:
  - Open/close portal access for clubs
  - Approve/reject club events
  - View all club activities
  - Manage attendance system

## How to Use

### For Club Leaders:
1. **Wait for Portal Access**: Contact VC to open portal for your club
2. **Collect Attendance**: Use Google Forms to collect student data
3. **Download Excel**: Download responses as Excel file
4. **Upload to System**: 
   - Login as club leader
   - Fill event details (name, date, period)
   - Upload Excel file with columns: Name, ID, Section, Year
5. **Wait for Approval**: VC will review and approve the attendance

### For Vice Chancellor:
1. **Open Portal**: 
   - Select club
   - Set duration (in hours)
   - Click "Open Portal"
2. **Review Events**:
   - Check pending event approvals
   - Verify uploaded attendance data
   - Approve or reject events
3. **Approved events automatically mark attendance in the system**

### For Students:
1. **View Dashboard**: See complete attendance records
2. **Check Statistics**: View attendance percentage
3. **Club Events**: Attendance marked via club events shows special badge

### For Teachers:
1. **Mark Attendance**: Select date, period, and present students
2. **Submit**: Attendance is saved for all students
3. **View History**: See today's attendance summary

## Excel File Format

The Excel file uploaded by clubs should have these columns:

| Name          | ID      | Section | Year |
|---------------|---------|---------|------|
| Rahul Kumar   | 2021001 | A       | 3    |
| Priya Sharma  | 2021002 | A       | 3    |
| Amit Singh    | 2021003 | A       | 3    |

## Database Schema

### Tables:
- **students**: Student information
- **teachers**: Teacher information
- **clubs**: Registered clubs
- **vc**: Vice Chancellor account
- **attendance**: Main attendance records
- **club_events**: Club event submissions
- **event_attendance**: Students who attended events
- **portal_access**: Portal access control

## Attendance Status Codes
- **P**: Present
- **A**: Absent
- **N.M.**: Not Mentioned (teacher didn't mark)

## Sample Data Included

### Students:
- 20 students (IDs: 2021001 to 2021020)
- Distributed across sections A, B, C
- All in Year 3

### Teachers:
- 5 teachers with different subjects
- Dr. Rajesh Kumar (Data Structures)
- Prof. Sunita Verma (Database Management)
- Dr. Anil Sharma (Computer Networks)
- Prof. Meena Gupta (Operating Systems)
- Dr. Prakash Singh (Web Technology)

### Clubs:
- Coding Club (CLUB001)
- Tech Fest Committee (CLUB002)
- Robotics Club (CLUB003)

### Attendance:
- 10 days of historical attendance data
- 5 periods per day
- Random distribution (70% present, 20% absent, 10% not marked)

## Technical Details

### Backend:
- **Framework**: Flask (Python)
- **Database**: SQLite
- **File Processing**: Pandas for Excel reading

### Frontend:
- **HTML5**: Templating with Jinja2
- **CSS3**: Custom responsive design
- **JavaScript**: Minimal (checkbox selection)

### Security Features:
- Session-based authentication
- Role-based access control
- File upload validation
- Secure filename handling

## Future Enhancements
1. Add face recognition for AI-based verification
2. Implement email notifications
3. Add export to PDF/Excel functionality
4. Real-time dashboard updates
5. Mobile app integration
6. Biometric integration

## Troubleshooting

### Database Issues:
```bash
# Delete existing database and recreate
rm attendance.db
python database.py
```

### Port Already in Use:
```bash
# Change port in app.py, last line:
app.run(debug=True, port=5001)
```

### Excel Upload Errors:
- Ensure Excel file has correct columns: Name, ID, Section, Year
- Check file extension (.xlsx or .xls)
- Verify portal is open for your club

## Support
For issues or questions, contact the system administrator.

## License
Educational project for college attendance management.