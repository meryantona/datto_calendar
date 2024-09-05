#Import necessary libraries
import streamlit as st
import sqlite3
import datetime
from utils import validate_date, validate_time, get_current_datetime, initialize
from event import Event
from PIL import Image

# Initt db
def init_db():
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 category TEXT,
                 label TEXT,
                 date TEXT,
                 time TEXT)''')
    conn.commit()
    conn.close()

# This must be at the start of the app
init_db()

# Page configuration
st.set_page_config(page_title="DATTO - Calendar App", layout="wide")

# Load image
image = Image.open('datto.jpg')

# Calculate new size while maintaining aspect ratio
max_width = 300  # Adjust this value as needed
ratio = max_width / float(image.size[0])
new_height = int(float(image.size[1]) * float(ratio))

# Resize image with high quality
resized_image = image.resize((max_width, new_height), Image.LANCZOS)

# Display image
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(resized_image, use_column_width=False)

# Sidebar for navigation
st.sidebar.title("DATTO - Calendar App")
page = st.sidebar.radio("MENU", ["Add Event", "Remove Event", "Change Event", "Show Events"])

# Add Event
if page == "Add Event":
    st.header("Add Event")
    category = st.selectbox("Category", ["Appointment", "Meeting", "Medical", "Free"])
    label = st.text_input("Label (2-50 characters)")
    date = st.date_input("Date")
    time = st.time_input("Time")
    
    if st.button("Add Event"):
        if 2 <= len(label) <= 50 and validate_date(date.strftime("%Y-%m-%d")) and validate_time(time.strftime("%H:%M")):
            new_event = Event(category, label, date.strftime("%Y-%m-%d"), time.strftime("%H:%M"))
            new_event.save_to_database()
            st.success("Event added successfully.")
        else:
            st.error("Invalid input. Please check your entries.")

# Remove Event
elif page == "Remove Event":
    st.header("Remove Event")
    events = Event.get_all_events()
    if events:
        event_to_remove = st.selectbox("Select event to remove", 
                                       [f"{e[3]} {e[4]} - {e[2]} ({e[1]})" for e in events])
        if st.button("Remove Event"):
            event_index = [f"{e[3]} {e[4]} - {e[2]} ({e[1]})" for e in events].index(event_to_remove)
            Event.remove_from_database(events[event_index][0])
            st.success("Event removed successfully.")
    else:
        st.info("No events to remove.")

# Change Event
elif page == "Change Event":
    st.header("Change Event")
    events = Event.get_all_events()
    if events:
        event_to_change = st.selectbox("Select event to change", 
                                       [f"{e[3]} {e[4]} - {e[2]} ({e[1]})" for e in events])
        new_date = st.date_input("New Date")
        new_time = st.time_input("New Time")
        
        if st.button("Change Event"):
            event_index = [f"{e[3]} {e[4]} - {e[2]} ({e[1]})" for e in events].index(event_to_change)
            Event.change_event_in_database(events[event_index][0], 
                                           new_date.strftime("%Y-%m-%d"), 
                                           new_time.strftime("%H:%M"))
            st.success("Event changed successfully.")
    else:
        st.info("No events to change.")

# Show Events
elif page == "Show Events":
    st.header("Show Events")
    interval = st.selectbox("Select time interval", 
                            ["One day", "One week", "One month", "Three months", "Six months"])
    
    today = datetime.datetime.now().date()
    if interval == "One day":
        end_date = today + datetime.timedelta(days=1)
    elif interval == "One week":
        end_date = today + datetime.timedelta(weeks=1)
    elif interval == "One month":
        end_date = today + datetime.timedelta(days=30)
    elif interval == "Three months":
        end_date = today + datetime.timedelta(days=90)
    else:
        end_date = today + datetime.timedelta(days=180)
    
    events = Event.get_events_in_interval(today, end_date)
    if events:
        for event in events:
            st.write(f"Date: {event[3]} - Time: {event[4]} || Label: {event[2]} || Category: {event[1]}")
    else:
        st.info("No events in the selected time interval.")

