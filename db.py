import sqlite3

class Database:
    def __init__(self, db): # python constructor which runs when an object is instantiated
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        # note primary key is id and not meeting_id as you might want to join same meeting for different times. Making meetin_id primary will allow only one unique entry for that meeting thus limiting ability to join same meeting for different time slots
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS meetings (id INTEGER PRIMARY KEY, meeting_id text, meeting_pwd text, meeting_start_time text, meeting_stop_time text)")
        self.connection.commit()

    # create
    def insert(self, meeting_id, meeting_pwd, meeting_start_time, meeting_stop_time):
        # setting primary key id to NULL as sqlite will auto assign value for it
        self.cursor.execute("INSERT INTO meetings VALUES (NULL, ?, ?, ?, ?)",
                         (meeting_id, meeting_pwd, meeting_start_time, meeting_stop_time))
        self.connection.commit()

    # read
    def fetch(self):
        self.cursor.execute("SELECT * FROM meetings") # select everything from meetings
        rows = self.cursor.fetchall() # fetch all rows
        return rows

    # update
    def update(self, id, meeting_id, meeting_pwd, meeting_start_time, meeting_stop_time):
        self.cursor.execute("UPDATE meetings SET meeting_id = ?, meeting_pwd = ?, meeting_start_time = ?, meeting_stop_time = ? WHERE id = ?",
                         (meeting_id, meeting_pwd, meeting_start_time, meeting_stop_time, id))
        self.connection.commit()

    # delete
    def delete(self, id):
        self.cursor.execute("DELETE FROM meetings WHERE id=?", (id,)) # trailing comma , is required as () is a python tuple with only one value
        self.connection.commit() 

    def __del__(self): # python destructor which runs when all references to an object have been deleted
        self.connection.close()

"""
# To check db class is working as expected
db = Database('meetings.db')
db.insert("9770788229", "VGEyTjNKbGJUYzkxRHdSaDkwaTZhdz09", "22:3", "22.4")
db.insert("6507456272", "cG5hYlN4dUg1Qk0xcEFMMHdJSk5ZQT09", "18:16", "18:23")
"""