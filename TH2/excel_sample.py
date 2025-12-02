# excel_sample.py
import pandas as pd

def generate_sample_excel(filename='sample_event_attendance.xlsx'):
    data = {
        'Name': [
            'Krishiv Karn','Rahul Sharma','Priya Singh','Amit Kumar','Neha Gupta',
            'Rohan Verma','Anjali Patel','Vikram Reddy','Sneha Desai','Arjun Mehta'
        ],
        'Student ID': [
            '25030175','25030176','25030177','25030178','25030179',
            '25030180','25030181','25030182','25030183','25030184'
        ],
        'Section': [
            'Section-J','Section-J','Section-J','Section-K','Section-K',
            'Section-J','Section-J','Section-K','Section-K','Section-J'
        ],
        'Year': [1]*10
    }
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, sheet_name='Event Attendance')
    print(f"Saved: {filename} ({len(df)} rows)")

if __name__ == '__main__':
    generate_sample_excel()
