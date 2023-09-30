import sqlite3


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS Employee(
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            doj TEXT,
            contact TEXT,
            address TEXT,
            username TEXT,
            password TEXT
        )"""
        self.cur.execute(sql)
        # Create the TimeIn table
        sql_times = """
                CREATE TABLE IF NOT EXISTS Timeseries(
                    employee_id INTEGER,
                    time_in_stamp TEXT,
                    time_out_stamp TEXT,
                    year INTEGER,
                    month INTEGER,
                    day INTEGER,
                    FOREIGN KEY (employee_id) REFERENCES Employee(id)
                )"""
        self.cur.execute(sql_times)


        # Commit the changes and close the database connection


        # Commit the changes and close the connectio
    def insert(self, name, age, gender, email, doj, contact, address, username, password):
        sql = ("INSERT INTO Employee (name, age, gender, email, doj, contact, address, username, password)"
               " VALUES (?,?,?,?,?,?,?,?,?)")
        values = (name, age, gender, email, doj, contact, address, username, password)
        self.cur.execute(sql, values)
        self.con.commit()

    def Fetch(self):
        self.cur.execute("SELECT * FROM Employee")
        rows = self.cur.fetchall()

        if not rows:  # Check if rows is empty
            print("None")  # Print "None" when there are no records
            return []  # Return an empty list

        return rows  # Return the list of rows

    def Delete(self, id):
        self.cur.execute("DELETE FROM Employee WHERE id=?", (id,))
        self.con.commit()

    def Update(self, id, name, age, gender, email, doj, contact, address, username, password):
        sql = "UPDATE Employee SET name=?,age=?,gender=?,email=?,doj=?,contact=?,address=?,username=?,password=? where id=?"
        updated_values = (name, age, gender, email, doj, contact, address, username, password, id)
        self.cur.execute(sql, updated_values)
        self.con.commit()

    def insert_timeseries(self, employee_id, time_in_stamp,time_out_stamp,year,month,day):
        sql = "INSERT INTO TimeIn (employee_id, time_in_stamp,time_out_stamp,year,month,day) VALUES (?,?,?,?,?,?)"
        values = (employee_id, time_in_stamp,time_out_stamp,year,month,day)
        self.cur.execute(sql, values)
        self.con.commit()






# Create an instance of the Database class
o = Database("Employee.db")
