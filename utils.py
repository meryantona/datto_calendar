import os
import sqlite3
import datetime

# Function to connect to the database
def connect_to_db():
    initialize()
    conn = sqlite3.connect('calendar.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def initialize():
    db_file = 'calendar.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 category TEXT,
                 label TEXT,
                 date TEXT,
                 time TEXT)''')
    conn.commit()
    conn.close()


# Function to create the database file
def create_db(db_file):
    conn = sqlite3.connect(db_file)
    conn.close()

# Function to validate date format (YYYY-MM-DD)
def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to validate time format (HH:MM)
def validate_time(time):
    try:
        datetime.datetime.strptime(time, '%H:%M')
        return True
    except ValueError:
        return False

# Function to get current date and time
def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
