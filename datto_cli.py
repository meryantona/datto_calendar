import os
import sqlite3
import datetime
from utils import connect_to_db, validate_date, validate_time, get_current_datetime
from event import Event


# Function to clear the terminal
def clear_terminal():
    os.system('clear')  # For Linux

# ANSI escape codes for styling
BOLD = "\033[1m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
BLINK = "\033[5m"
RESET = "\033[0m"  # Reset styling


# Function to display colored banner
def print_banner():
    print(YELLOW)
    print("""
    ██████╗     ███╗    ██████╗  ██████╗  ███████╗ 
    ██╔══██╗   ██║██╗     ██╗      ██╗    ██╔══██╗
    ██║  ██║  ███████║    ██╗      ██╗    ██╔══██╗
    ██║  ██║  ██║  ██║    ██╗      ██╗    ██╔══██╗
    ██████╔╝  ██║  ██║    ██╗      ██╗    ███████╗
    ╚═════╝   ╚═╝  ╚═╝    ╚═╝      ╚═╝    ╚══════╝
    ════             Calendar App             ════
    \033[0m""")  # Reset color for ASCII art


# Function to display current date and time
def print_current_datetime_intro():
    current_datetime = get_current_datetime()
    styled_text = f"{BOLD}{BLUE}Welcome to DATTO - Current Date and Time:{RESET} {BOLD}{current_datetime}{RESET}"
    print(styled_text)

def print_current_datetime():
    current_datetime = get_current_datetime()
    styled_text2 = f"{BOLD}{BLUE}Current Date and Time:{RESET} {BOLD}{current_datetime}{RESET}"
    print(styled_text2)

# Initialize SQLite database connection
conn = sqlite3.connect('calendar.db')
c = conn.cursor()

# Create events table in the database
c.execute('''CREATE TABLE IF NOT EXISTS events
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             category TEXT,
             label TEXT,
             date TEXT,
             time TEXT,
             encrypted_data TEXT)''')

# Commit changes and close connection
conn.commit()
conn.close()

# Menu for actions
def print_menu():
    print("\n" + BOLD + "Main Menu:" + RESET + "\n")
    print("1. Add Event")
    print("2. Remove Event")
    print("3. Change Event")
    print("4. Show Event")
    print("5. Exit")
    print("\n" + "-" * 30)

# Define add_event function
def add_event(category, label, date, time):
    # Connect to the SQLite database
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()

    # Insert event details into the database
    c.execute("INSERT INTO events (category, label, date, time) VALUES (?, ?, ?, ?)",
              (category, label, date, time))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(GREEN + "\nEvent added successfully." + RESET)

# Function to handle user input and display events based on the selected time interval
def show_event():
    def show_events_in_interval(start_date, end_date):
        # Initialize SQLite database connection
        conn = sqlite3.connect('calendar.db')
        c = conn.cursor()

        # Retrieve events within the specified time interval
        c.execute("SELECT * FROM events WHERE date BETWEEN ? AND ?", (start_date, end_date))
        events = c.fetchall()

        # Close connection
        conn.close()

        # Return events if there are any, otherwise return None
        if events:
            return events
        else:
            return None

    # Display menu for time interval options
    print_current_datetime()
    print(BOLD + "\nShow Events:" + RESET)
    print("1. Show events for one day")
    print("2. Show events for one week")
    print("3. Show events for one month")
    print("4. Show events for three months")
    print("5. Show events for the next six months")
    print("6. Go back")
    print()

    while True:
        choice = input(BOLD + "Enter your choice (1-6): " + RESET)
        if choice in ['1', '2', '3', '4', '5']:
            today = datetime.datetime.now().date()
            if choice == "1":
                end_date = today + datetime.timedelta(days=1)
            elif choice == "2":
                end_date = today + datetime.timedelta(weeks=1)
            elif choice == "3":
                end_date = today + datetime.timedelta(days=30)
            elif choice == "4":
                end_date = today + datetime.timedelta(days=90)
            elif choice == "5":
                end_date = today + datetime.timedelta(days=180)

            # Check if there are events in the selected time interval
            events = show_events_in_interval(today, end_date)
            if events is None:
                print(YELLOW + "No events in that time interval.\n" + RESET)
            else:
                print(BLUE + "Showing Events from:" + RESET, today, BLUE + "To:" + RESET, end_date)
                print()
                for event in events:
                    print(f"{BOLD}Date:{RESET} {event[3]} - {BOLD}Time:{RESET} {event[4]}  || {BOLD}Label:{RESET} {event[2]} || {BOLD}Category:{RESET} {event[1]}")
        elif choice == "6":
            break
        else:
            print(RED + "\nInvalid choice. Please enter a number between 1 and 6." + RESET)

# Function to show all events without specifying a time interval
def show_all_events():
    confirm = input("Do you want to show all events? (y/n): ")
    if confirm.lower() == 'y':
        events = Event.get_all_events()
        if events:
            # Sort events by date and time
            events.sort(key=lambda x: x[3] + " " + x[4])
            print(BOLD + "\nAll the events saved:" + RESET)
            for i, event in enumerate(events, 1):
                print(f"{i}. {event[3]} {event[4]} || {BOLD}Label:{RESET} {event[2]} || {BOLD}Category:{RESET} {event[1]}")
            return events
        else:
            print("No events found.")
            return []
    else:
        return []

#Function for changing category menu not in use
def change_category_submenu(category_mapping):
    print("Current category:", category_mapping[event_to_change[1]])
    print("\nSelect a new category:")
    print("1. Appointment")
    print("2. Meeting")
    print("3. Medical")
    print("4. Free")
    print("\n" + "-" * 30)
    new_category_choice = input("Enter your choice: ")
    if new_category_choice in category_mapping:
        new_category = category_mapping[new_category_choice]
        return new_category
    else:
        print(RED + "Invalid category choice. Keeping the existing category." + RESET)
        return event_to_change[1]  # Keep the existing category



# Main function
def main():
    clear_terminal()
    print_banner()
    print_current_datetime_intro()

    # Main loop for user interaction
    while True:
        print_menu()
        choice = input(BOLD + "Enter your choice: " + RESET)

        if choice == "1":
            print()
            # Add Event Function
            print(BOLD + "\nSelect a category for the new event:" + RESET)
            print("-" * 30)
            print("1. Appointment")
            print("2. Meeting")
            print("3. Medical")
            print("4. Free")
            print("-" * 30)

            # Prompt the user to choose a category
            while True:
                category_choice = input("Enter the number corresponding to the category: ")
                if category_choice in ['1', '2', '3', '4']:
                    break
                else:
                    print(RED + "Invalid choice. Please enter a number between 1 and 4.\n" + RESET)

            # Map the user's choice to the corresponding category
            category_mapping = {'1': 'Appointment', '2': 'Meeting', '3': 'Medical', '4': 'Free'}
            category = category_mapping[category_choice]

            # Prompt the user for a label with validation
            while True:
                label = input("Enter a label for the event (2-50 characters): ")
                if 2 <= len(label) <= 50:
                    break
                else:
                    print(RED + "Invalid label length. Label must be between 2 and 50 characters.\n" + RESET)

            # Prompt the user for a valid date
            while True:
                date = input("Enter the date of the event (format: yyyy-mm-dd): ")
                if validate_date(date):
                    break
                else:
                    print(RED + "Invalid date format. Please enter a date in the format yyyy-mm-dd.\n" + RESET)

            # Prompt the user for a valid time
            while True:
                time = input("Enter the time of the event (format: hh:mm): ")
                if validate_time(time):
                    break
                else:
                    print(RED + "Invalid time format. Please enter a time in 24-hour format (hh:mm).\n" + RESET)

            add_event(category, label, date, time)

        #Remove event
        elif choice == "2":
            print()
            events = show_all_events()
            if events:
                event_index = input(BOLD + "\nEnter the number of the event you want to remove: " + RESET)
                try:
                    event_index = int(event_index)  # Convert to integer
                    if 1 <= event_index <= len(events):
                        event_to_remove = events[event_index - 1]
                        event_id = event_to_remove[0]  # Extract event ID from the event data
                        print(f"{BOLD}\nEvent to remove:{RESET}\n"
                              f"{BOLD}Date:{RESET} {event_to_remove[3]} {event_to_remove[4]}|| "
                              f"{BOLD}Label:{RESET} {event_to_remove[2]}|| "
                              f"{BOLD}Category:{RESET} {event_to_remove[1]}")
                        confirm_remove = input(YELLOW + "\nAre you sure you want to remove this event? (y/n): " + RESET)
                        if confirm_remove.lower() == 'y':
                            Event.remove_from_database(event_id)
                            print(GREEN + "Event removed successfully.\n" + RESET)
                        else:
                            print(YELLOW + "Event removal canceled.\n" + RESET)
                    else:
                        print(RED + "Invalid event number. Please enter a valid number.\n" + RESET)
                except ValueError:
                    print(RED + "Invalid event number. Please enter a valid integer number.\n" + RESET)
                except Exception as e:
                    print(RED + "An error occurred:\n" + RESET, e)

        elif choice == "3":
            print()
            events = show_all_events()  # Show all events
            if events:
                event_index = input(BOLD + "\nEnter the number of the event you want to change: " + RESET)
                print("\n" + "-" * 30)
                try:
                    event_index = int(event_index)  # Convert to integer
                    if 1 <= event_index <= len(events):
                        event_to_change = events[event_index - 1]
                        event_id = event_to_change[0]  # Extract event ID from the event data
                        print(f"{BOLD}\nEvent to change:{RESET}\n"
                              f"{BOLD}Date:{RESET} {event_to_change[3]} {event_to_change[4]}|| "
                              f"{BOLD}Label:{RESET} {event_to_change[2]}|| "
                              f"{BOLD}Category:{RESET} {event_to_change[1]} ")
                        confirm_change = input(YELLOW + "Are you sure you want to change this event? (y/n): \n" + RESET)
                        if confirm_change.lower() == 'y':
                            new_date = input("Enter the new date (YYYY-MM-DD): ")
                            new_time = input("Enter the new time (HH:MM): ")
                            # Update event details if user confirms
                            if new_date and validate_date(new_date) and new_time and validate_time(new_time):
                                Event.change_event_in_database(event_id, new_date, new_time)
                                print(GREEN + "Event changed successfully.\n" + RESET)
                            else:
                                print(RED + "Invalid date or time format.\n" + RESET)
                        else:
                            print(YELLOW + "Event change canceled.\n" + RESET)
                except Exception as e:
                    print(RED + "An error occurred:\n" + RESET, e)

        elif choice == "4":
            print()
            show_event()

        elif choice == "5":
            print()
            print(BLUE + "\nExiting DATTO - Calendar Application. Goodbye!\n" + RESET)
            break
        else:
            print(RED + "Invalid choice. Please enter a valid option." + RESET)

# Entry point of the script
if __name__ == "__main__":
    main()
