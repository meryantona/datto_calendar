import sqlite3

class Event:
    def __init__(self, category, label, date, time):
        self.category = category
        self.label = label
        self.date = date
        self.time = time

    # Method to save the event to the database
    def save_to_database(self):
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()

        # Insert event details into the database
        cursor.execute("INSERT INTO events (category, label, date, time) VALUES (?, ?, ?, ?)",
                       (self.category, self.label, self.date, self.time))

        conn.commit()
        conn.close()

    # Methods for remove, change, and retrieve events remain the same...

    # Method to remove the event from the database
    @staticmethod
    def remove_from_database(event_id):
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
            conn.commit()
        except sqlite3.Error as e:
            print("Error occurred while removing the event:", e)
        finally:
            conn.close()

    @staticmethod
    def change_event_in_database(event_id, new_date, new_time):
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        try:
            # Build the SQL update query based on the user's input
            sql = "UPDATE events SET date = ?, time = ?,"
            params = [new_date, new_time]

            # Remove the trailing comma and complete the SQL query
            sql = sql.rstrip(',') + " WHERE id = ?"
            params.append(event_id)

            # Print the generated SQL query and parameters for debugg
            # print("Generated SQL query:", sql)
            # print("Parameters:", params)

            # Execute the SQL query
            cursor.execute(sql, params)
            conn.commit()
            print("Event details updated in the database.")
        except sqlite3.Error as e:
            print("Error occurred while changing event details:", e)
        finally:
            conn.close()

    # Method to retrieve all events from the database
    @staticmethod
    def get_all_events():
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        conn.close()
        return events

    # Method to retieve events in interval
    @staticmethod
    def get_events_in_interval(start_date, end_date):
        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE date BETWEEN ? AND ?", (start_date, end_date))
        events = cursor.fetchall()
        conn.close()
        return events
