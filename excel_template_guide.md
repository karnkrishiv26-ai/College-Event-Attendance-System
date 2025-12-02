# Excel File Template Guide for Club Leaders

## Google Form Setup

When creating your Google Form for event attendance, include these questions:

1. **Full Name** (Short answer)
2. **Student ID** (Short answer)
3. **Section** (Multiple choice: A, B, C)
4. **Year** (Multiple choice: 1, 2, 3, 4)

## Downloading from Google Forms

1. Open your Google Form responses
2. Click on the **Google Sheets** icon (green spreadsheet icon)
3. In the spreadsheet, go to **File → Download → Microsoft Excel (.xlsx)**
4. Save the file to your computer

## Expected Excel Format

Your downloaded Excel file should look like this:

| Timestamp           | Name          | ID      | Section | Year |
|---------------------|---------------|---------|---------|------|
| 12/1/2024 10:30:00 | Rahul Kumar   | 2021001 | A       | 3    |
| 12/1/2024 10:31:15 | Priya Sharma  | 2021002 | A       | 3    |
| 12/1/2024 10:32:45 | Amit Singh    | 2021003 | A       | 3    |

**Note:** The system will read columns named: `Name`, `ID`, `Section`, `Year`

## Required Columns

### 1. Name
- **Type**: Text
- **Example**: "Rahul Kumar"
- **Rules**: Full name of the student

### 2. ID
- **Type**: Text/Number
- **Example**: "2021001"
- **Rules**: Must match the student ID in the system database

### 3. Section
- **Type**: Text
- **Example**: "A", "B", or "C"
- **Rules**: Single character section identifier

### 4. Year
- **Type**: Number
- **Example**: 3
- **Rules**: Year of study (1, 2, 3, or 4)

## Common Issues and Solutions

### Issue 1: Column Names Don't Match
**Problem**: Excel has "Student Name" instead of "Name"
**Solution**: Rename the column header to exactly "Name" (case-sensitive)

### Issue 2: Extra Columns
**Problem**: Excel has timestamp, email, etc.
**Solution**: No problem! The system only reads the 4 required columns

### Issue 3: Student ID Not Found
**Problem**: System says "Student not found"
**Solution**: Verify the ID exists in the database (check with admin)

### Issue 4: Portal Closed
**Problem**: "Portal access is not active"
**Solution**: Contact VC to open portal access for your club

## Step-by-Step Upload Process

### Step 1: Prepare Excel File
- Ensure all 4 columns are present: Name, ID, Section, Year
- Remove any unnecessary rows or formatting
- Save as .xlsx or .xls format

### Step 2: Login to System
- Go to the attendance system website
- Login with your club credentials
- Select "Club Leader" as role

### Step 3: Check Portal Status
- Look for "Portal Access Status" section
- If closed, contact VC
- If open, proceed to upload

### Step 4: Upload Attendance
- Fill in Event Name (e.g., "Hackathon 2024")
- Select Event Date
- Choose Period (which class period students missed)
- Click "Choose File" and select your Excel file
- Click "Upload Attendance"

### Step 5: Wait for Approval
- VC will review your submission
- Check "Event History" section for status
- Once approved, attendance is automatically marked

## Sample Excel Data

Here's sample data you can use to test:

```
Name,ID,Section,Year
Rahul Kumar,2021001,A,3
Priya Sharma,2021002,A,3
Amit Singh,2021003,A,3
Sneha Gupta,2021004,B,3
Rohan Verma,2021005,B,3
Anjali Patel,2021006,B,3
Vijay Kumar,2021007,C,3
Neha Singh,2021008,C,3
Karan Mehta,2021009,C,3
Pooja Reddy,2021010,A,3
```

## Tips for Success

1. **Double-check Student IDs**: Wrong IDs will cause errors
2. **Consistent Format**: Always use the same column names
3. **Clean Data**: Remove duplicate entries before uploading
4. **Timely Upload**: Upload soon after the event while portal is open
5. **Communicate with VC**: Inform VC before major events

## Event Types Examples

### Workshop/Seminar
- Period: 1-2 (morning sessions)
- Upload immediately after event

### Hackathon
- Period: All day (mark for each period)
- May need multiple uploads for different periods

### Club Meeting
- Period: Specific time slot
- Regular recurring events

### Competition
- Period: Competition duration
- Include only participants, not audience

## Support

If you encounter issues:
1. Check this guide first
2. Verify Excel format matches template
3. Ensure portal is open
4. Contact system administrator
5. Reach out to VC office

## Quick Reference

| What | Format |
|------|--------|
| File Type | .xlsx or .xls |
| Required Columns | Name, ID, Section, Year |
| Max File Size | 16 MB |
| Portal Access | Must be open by VC |
| Approval Time | Within 24-48 hours |

---

**Remember**: This system helps track club participation while ensuring students get attendance credit for college activities. Use it responsibly!