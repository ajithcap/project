import sqlite3
import random
import string
from tkinter import filedialog
import tkinter as tk

import pandas as pd

# Connect to the database (make sure your database file exists)
conn = sqlite3.connect('Employee.db')
cursor = conn.cursor()

# Define the number of records you want to generate
num_records = 1000  # You can adjust this number as needed

# Create the table if it doesn't exist (you can omit this if the table already exists)
cursor.execute('''
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
    )
''')

# Generate and insert random data into the table
for _ in range(num_records):
    name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    age = random.randint(20, 60)
    gender = random.choice(['Male', 'Female'])
    email = f'{name.lower()}@example.com'
    doj = f'2023-09-{random.randint(1, 30)}'
    contact = ''.join(random.choice(string.digits) for _ in range(10))
    address = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    username = name.lower()
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    cursor.execute('''
        INSERT INTO Employee (name, age, gender, email, doj, contact, address, username, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, gender, email, doj, contact, address, username, password))

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f'Generated {num_records} records.')



def import_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if not file_path:
        return  # User canceled the file dialog

    try:
        # Read the selected CSV file into a Pandas DataFrame
        df = pd.read_csv(file_path)

        # Optionally, you can perform additional processing here
        # For example, you can clean the data, convert data types, etc.

        # Return the DataFrame
        return df

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Create a Tkinter window
root = tk.Tk()
root.title("CSV File Import")
root.geometry("400x200")

# Create a button to trigger CSV file import
import_button = tk.Button(root, text="Import CSV File", command=import_csv_file)
import_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
