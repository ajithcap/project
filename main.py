import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END, messagebox, filedialog
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from db import Database
from tkcalendar import DateEntry
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

db = Database("Employee.db")
conn = sqlite3.connect('Employee.db')

root = tk.Tk()
root.title("emp")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
# Create a custom title bar


def open_welcome_page():
    welcome_window = tk.Toplevel(root)
    welcome_window.title("Welcome Page")
    welcome_window.config(bg="peach puff")

    # Customize the welcome page
    welcome_label = tk.Label(welcome_window, text=f"Welcome, {username_var.get()}!", bg="peach puff")
    welcome_label.pack()

    # Frame for ID, Date, and Time-In
    input_frame = tk.Frame(welcome_window, bg="light blue")
    input_frame.pack(pady=20, )

    # ID Entry
    id_label = tk.Label(input_frame, text="Enter ID:", bg="light blue")
    id_label.grid(row=1, column=1, padx=10, pady=5)
    id_entry = tk.Entry(input_frame)
    id_entry.grid(row=1, column=2, padx=10, pady=5)

    # Date Label
    date_label = tk.Label(input_frame, text="Select Date:", bg="light blue")
    date_label.grid(row=3, column=1, padx=10, pady=5)

    # Date Entry using tkcalendar's DateEntry widget
    date_entry = DateEntry(input_frame, date_pattern="yyyy-mm-dd", bg="light blue")
    date_entry.grid(row=3, column=2, padx=10, pady=5)
    # Destroy the calendar widget to clear the date selection

    # Time-In Entry (Using Spinbox)
    # Time-In Entry (Using Spinbox)
    time_in_label = tk.Label(input_frame, text="Enter Time-In (hh:mm AM/PM):", bg="light blue")
    time_in_label.grid(row=1, column=3, padx=10, pady=5)

    # Create a Spinbox for time-in with 12-hour format and AM/PM
    time_in_spinbox = tk.Spinbox(input_frame,
                                 values=[
                                     f"{hour:02d}:{minute:02d} AM" if hour < 12 else f"{hour - 12:02d}:{minute:02d} PM" if hour > 12 else f"{hour:02d}:{minute:02d} PM"
                                     for hour in range(1, 13) for minute in
                                     [0, 15, 30, 45]],
                                 increment=1)
    time_in_spinbox.grid(row=2, column=3, padx=10, pady=5)

    # Time-Out Entry (Using Spinbox)
    time_out_label = tk.Label(input_frame, text="Enter Time-Out (hh:mm AM/PM):", bg="light blue")
    time_out_label.grid(row=3, column=3, padx=10, pady=5)

    # Create a Spinbox for time-out with 12-hour format and AM/PM
    time_out_spinbox = tk.Spinbox(input_frame,
                                  values=[
                                      f"{hour:02d}:{minute:02d} AM" if hour < 12 else f"{hour - 12:02d}:{minute:02d} PM" if hour > 12 else f"{hour:02d}:{minute:02d} PM"
                                      for hour in range(1, 13) for minute in
                                      [0, 15, 30, 45]],
                                  increment=1)
    time_out_spinbox.grid(row=4, column=3, padx=10, pady=5)

    def enter_data():
        entered_id = id_entry.get()
        entered_date = date_entry.get()
        entered_time_in = time_in_spinbox.get().replace(" ", ":")  # Replace space with ':'
        entered_time_out = time_out_spinbox.get().replace(" ", ":")  # Replace space with ':'

        parsed_date = datetime.strptime(entered_date, "%Y-%m-%d")
        year = parsed_date.year
        month = parsed_date.month
        day = parsed_date.day

        # Create an instance of the Database class with the database file "Employee.db"
        db = Database("Employee.db")

        # Insert data into the Employee table
        # db.insert(entered_id, '', '', '', '', '', '', '', '')

        # Insert time-in data into the Timeseries table with the selected date
        db.insert_timeseries(entered_id, entered_time_in, entered_time_out, year, month, day)

        id_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)  # Clear the selected date
        time_in_spinbox.delete(0, tk.END)  # Clear time-in selection (set to default time)
        time_out_spinbox.delete(0, tk.END)  # Clear time-out selection (set to default time)

    # Clear time-out selection (set to default time)

    # Clear time-out selection (set to default time)

    enter_button = tk.Button(input_frame, text="Enter", command=enter_data, bg="medium purple")
    enter_button.grid(row=7, column=2, padx=10, pady=10)

    def logout():
        welcome_window.destroy()  # Close the welcome window

    logout_button = tk.Button(input_frame, text="Logout", command=logout, bg="deep pink2")
    logout_button.grid(row=7, column=3, pady=10)


# Call the function to open the welcome page
def validate_login():
    username = username_var.get()
    password = password_var.get()

    conn = sqlite3.connect('Employee.db')
    cursor = conn.cursor()

    # Query the database for the entered username and password
    cursor.execute("SELECT * FROM Employee WHERE username=? AND password=?", (username, password))
    user_data = cursor.fetchone()

    if username == "ajith" and password == "ak":
        # Valid credentials for ajith and ak, open the main program
        root.deiconify()  # Show the main program window
        open_main_program()
        login_window.withdraw()
        # Hide the login window
    elif user_data:
        login_window.withdraw()
        open_welcome_page()
    else:

        messagebox.showerror("Login Failed", "Invalid username or password")


# Create a frame for the log
# Start the main GUI loop


# Entry frame var
name = tk.StringVar()
age = tk.StringVar()
gender = tk.StringVar()
email = tk.StringVar()
doj = tk.StringVar()
address = tk.StringVar()
contact = tk.StringVar()
username = tk.StringVar()
password = tk.StringVar()

# Button var
add = tk.StringVar()
update = tk.StringVar()
delete = tk.StringVar()

# Create a style for ttk widgets
style = ttk.Style()
style.configure("TFrame", background="forestgreen")
style.configure("TLabel", background="forestgreen", foreground="LightGoldenRodYellow", font=("Arial", 20))

# Creating the frame namely entries_frame
entries_frame = ttk.Frame(root)
entries_frame.grid(row=1, column=0, sticky="nsew")

title = ttk.Label(entries_frame, text="Employee Table", background="indigo", foreground="white")
title.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky="N")
title.config(font=("Arial", 30))
# Name
lbName = ttk.Label(entries_frame, text="Name")
lbName.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
txName = ttk.Entry(entries_frame, textvariable=name, width=30)
txName.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Age
lbAge = ttk.Label(entries_frame, text="Age")
lbAge.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
txAge = ttk.Entry(entries_frame, textvariable=age, width=30)
txAge.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# Gender
lbGen = ttk.Label(entries_frame, text="Gender")
lbGen.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
coGen = ttk.Combobox(entries_frame, width=27, textvariable=gender, state="readonly")
coGen['values'] = ("Male", "Female")
coGen.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Date of Joining
lbDoj = ttk.Label(entries_frame, text="Date of Joining")
lbDoj.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
txDoj = ttk.Entry(entries_frame, textvariable=doj, width=30)
txDoj.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Email
lbEmail = ttk.Label(entries_frame, text="Email")
lbEmail.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")
txEmail = ttk.Entry(entries_frame, textvariable=email, width=30)
txEmail.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

# username
lbuse = ttk.Label(entries_frame, text="USERNAME")
lbuse.grid(row=1, column=5, padx=20, pady=10, sticky="nsew")
txuse = ttk.Entry(entries_frame, textvariable=username, width=30)
txuse.grid(row=1, column=6, padx=10, pady=10, sticky="nsew")

# password
lbpas = ttk.Label(entries_frame, text="PASSWORD")
lbpas.grid(row=2, column=5, padx=20, pady=10, sticky="nsew")
txpas = ttk.Entry(entries_frame, textvariable=password, width=30)
txpas.grid(row=2, column=6, padx=10, pady=10, sticky="nsew")

# Contact
lbCnt = ttk.Label(entries_frame, text="Contact")
lbCnt.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")
txCnt = ttk.Entry(entries_frame, textvariable=contact, width=30)
txCnt.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

# Address
lbAdd = ttk.Label(entries_frame, text="Address")
lbAdd.grid(row=3, column=2, padx=20, pady=10, sticky="nsew")
txAdd = tk.Text(entries_frame, width=40, height=5)
txAdd.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

# time tracking
# ...
# Your previous code

# time tracking

# Rest of your code

# Load your image using PIL
image = Image.open("ems.jpg")  # Replace "your_image.png" with your image file path
image = image.resize((200, 200))  # Resize the image if needed

# Convert the PIL image to a PhotoImage object (Tkinter-compatible)
tk_image = ImageTk.PhotoImage(image)

# Create a Label to display the image
image_label = tk.Label(root, image=tk_image)
image_label.place(x=1700, y=10)  # Adjust the coordinates to position the image as desired

df = pd.read_sql_query("SELECT * FROM Employee", conn)


def open_main_program():
    def analyze_gender_distribution():
        # Ensure that 'df' is accessible within this function
        global df
        conn = sqlite3.connect('Employee.db')

        selected_gender = gender.get()
        print("Selected Gender:", selected_gender)  # Add this line for debugging
        df = pd.read_sql_query("SELECT * FROM Employee", conn)
        print("Data from Database:", df)
        # Calculate gender distribution, create pie chart, and display statistics
        total_employees = len(df)
        male_employees = len(df[df['gender'] == 'Male'])
        female_employees = len(df[df['gender'] == 'Female'])
        percentage_male = (male_employees / total_employees) * 100
        percentage_female = (female_employees / total_employees) * 100
        df['Gender Distribution'] = ''
        df.loc[df['gender'] == 'Male', 'Gender Distribution'] = 'Male'
        df.loc[df['gender'] == 'Female', 'Gender Distribution'] = 'Female'

        # Create a pie chart to visualize the gender distribution
        plt.figure(figsize=(6, 6))
        gender_distribution_counts = df['Gender Distribution'].value_counts()
        plt.pie(gender_distribution_counts, labels=gender_distribution_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Gender Distribution Among Employees')

        # Display gender distribution statistics
        gender_stats_text = f"Total Employees: {total_employees}\n" \
                            f"Male Employees: {male_employees} ({percentage_male:.2f}%)\n" \
                            f"Female Employees: {female_employees} ({percentage_female:.2f}%)"
        messagebox.showinfo("Gender Distribution Statistics", gender_stats_text)

    # ... (The rest of your code for GUI setup)

    # Create a button to trigger the gender distribution analysis
    gender_analysis_button = tk.Button(entries_frame, text="Analyze Gender Distribution",
                                       command=analyze_gender_distribution,
                                       padx=10, pady=20, width=20, bg="cyan2", borderwidth=0)
    gender_analysis_button.place(x=1400, y=100)

    def count_employees_joined_after(doj_date):
        try:
            # Create or connect to the SQLite database (use your database name)
            conn = sqlite3.connect('Employee.db')
            cur = conn.cursor()

            # Define the SQL query to count employees who joined after the specified DOJ date
            query = f"SELECT COUNT(*) FROM Employee WHERE doj > '{doj_date}'"

            # Execute the query
            cur.execute(query)

            # Fetch the result
            count = cur.fetchone()[0]

            # Close the database connection
            conn.close()

            return count

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return 0  # Return 0 in case of an error

    def calculate_tenure():
        # Get the Date of Joining (DOJ) from the form
        doj_text = doj.get()

        # Check if the DOJ field is empty
        if not doj_text:
            messagebox.showwarning("Tenure Calculation", "Please enter the Date of Joining.")
            return

        try:
            # Call the count_employees_joined_after function to get the count
            employees_count = count_employees_joined_after(doj_text)

            # Display the count of employees who joined after the specified DOJ date in a messagebox
            result_message = f"Number of employees who joined after {doj_text}:  {employees_count}"
            messagebox.showinfo("Employee Count", result_message)

        except ValueError:
            messagebox.showerror("Date Error", "Please enter a valid Date of Joining in the format YYYY-MM-DD.")

    # ... (The rest of your GUI setup and code)

    tenure_button = tk.Button(entries_frame, text="Calculate Tenure", command=calculate_tenure,
                              padx=10, pady=20, bg="thistle1", borderwidth=0, width=20)
    tenure_button.place(x=1400, y=200)

    def import_csv_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            return  # User canceled the file dialog

        try:
            # Read the selected CSV file into a Pandas DataFrame
            df = pd.read_csv(file_path)

            # Create or connect to the SQLite database (use your database name)
            conn = sqlite3.connect('Employee.db')

            # Get the list of columns in the DataFrame
            columns = df.columns.tolist()

            # Get the existing table's column names
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(Employee)")
            existing_columns = [column[1] for column in cursor.fetchall()]
            cursor.close()

            # Check if all columns in the DataFrame exist in the existing table
            if not all(col in existing_columns for col in columns):
                messagebox.showwarning("CSV Import Warning",
                                       "The CSV file contains columns that do not match the table's columns.")
                return  # Exit without importing if columns don't match

            # Create a table in the database with the same column names as in the CSV file
            create_table_sql = f"CREATE TABLE IF NOT EXISTS Employee ({', '.join([f'{col} TEXT' for col in columns])})"
            conn.execute(create_table_sql)

            # Insert the data from the DataFrame into the "Employee" table
            df.to_sql('Employee', conn, if_exists='append', index=False)

            conn.commit()
            conn.close()
            displayAll()
            messagebox.showinfo("CSV Import", "Data imported successfully.")

        except FileNotFoundError:
            messagebox.showerror("CSV Import Error", f"File not found: {file_path}")
        except Exception as e:
            messagebox.showerror("CSV Import Error", f"An error occurred: {str(e)}")

    # Create a button for importing CSV data

    def getData(self):
        select_row = tv.focus()
        data = tv.item(select_row)
        global row
        row = data["values"]

        if row and len(row) > 1:
            name.set(row[1])
            age.set(row[2])
            gender.set(row[3])
            email.set(row[4])
            doj.set(row[5])
            txAdd.delete(1.0, END)
            txAdd.insert(END, row[7])
            contact.set(row[6])
            username.set(row[8])
            password.set(row[9])
        else:
            # Handle the case where row doesn't contain the expected data
            messagebox.showerror("Error", "Selected row does not contain valid data")

    # Create a label to display the message
    message_label = tk.Label(entries_frame, text="", fg="violetred4", background="forestgreen", font=("cabiliri", 20))
    message_label.grid(row=6, column=10, columnspan=4, rowspan=3, padx=20, pady=20, sticky="nsew")

    # Function to center the message label

    # Modify the displayAll function
    def displayAll():
        rows = db.Fetch()  # Fetch records from the database
        tv.delete(*tv.get_children())
        if not rows:  # Check if there are no records
            message_label.config(text="Empty !")  # Update the message label with "None"
        else:
            message_label.config(text="")  # Clear the message label
            for row in rows:
                tv.insert("", END, values=row)

    message_frame = ttk.Frame(entries_frame)
    message_frame.grid(row=5, column=5, padx=10, pady=10)

    # Create a label for the message
    message_label = ttk.Label(message_frame, text="", font=("Arial", 20), foreground="firebrick4", borderwidth=2)
    message_label.pack()

    def update_db():
        try:
            if not all([txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(), txCnt.get(),
                        txAdd.get("1.0", "end-1c"), txuse.get(), txpas.get()]):
                messagebox.showerror("Error in input", "Please fill all the details")
                return

            # Get the currently selected row in the Treeview
            select_row = tv.focus()
            data = tv.item(select_row)
            selected_row = data["values"]

            # Get the address text from the Text widget
            address_text = txAdd.get("1.0", "end-1c")

            # Set each value individually based on the entry fields and ComboBox
            selected_row[1] = txName.get()
            selected_row[2] = txAge.get()
            selected_row[3] = coGen.get()
            selected_row[4] = txEmail.get()
            selected_row[5] = txDoj.get()
            selected_row[6] = txCnt.get()
            selected_row[7] = address_text
            selected_row[8] = txuse.get()
            selected_row[9] = txpas.get()

            # Update the Treeview with the modified values
            tv.item(select_row, values=selected_row)

            # Get the ID of the selected row
            selected_id = selected_row[0]

            # Update the record in the database
            db.Update(selected_id, txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(),
                      txCnt.get(), address_text, txuse.get(), txpas.get())

            messagebox.showinfo("Success", "Record updated")
            clear_db()
            displayAll()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while updating the record: {str(e)}")

    def add_db():
        try:
            if not all([txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(), txCnt.get(),
                        txAdd.get("1.0", "end-1c"), txuse.get(), txpas.get()]):
                messagebox.showerror("Error in input", "Please fill all the details")
                return

            # Get the address text from the Text widget
            address_text = txAdd.get("1.0", "end-1c")

            # Use the address_text variable when inserting into the database
            db.insert(txName.get(), txAge.get(), coGen.get(), txEmail.get(), txDoj.get(), txCnt.get(), address_text,
                      txuse.get(), txpas.get())

            messagebox.showinfo("Success", "Record inserted")
            clear_db()
            displayAll()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while inserting the record: {str(e)}")

    def delete_db():
        db.Delete(row[0])
        clear_db()
        displayAll()

    def clear_db():
        name.set("")
        age.set("")
        gender.set("")
        email.set("")
        doj.set("")
        txAdd.delete(1.0, END)
        contact.set("")
        username.set("")
        password.set("")

    # Creating a button frame
    # Creating a button frame
    btFrame = tk.Frame(entries_frame, bg="forestgreen", borderwidth=0)
    btFrame.grid(row=7, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

    btUpdate = tk.Button(btFrame, text="Update", command=update_db, padx=10, pady=20, width=15, bg="lightgreen",
                         borderwidth=0)
    btUpdate.grid(row=0, column=0, padx=10)

    btAdd = tk.Button(btFrame, text="Add", command=add_db, padx=10, pady=20, width=15, bg="gold", borderwidth=0)
    btAdd.grid(row=0, column=1, padx=10)

    btDelete = tk.Button(btFrame, text="Delete", command=delete_db, padx=10, pady=20, width=15, bg="red", borderwidth=0)
    btDelete.grid(row=0, column=2, padx=10)

    btClear = tk.Button(btFrame, text="Clear", command=clear_db, padx=10, pady=20, width=15, bg="grey", borderwidth=0)
    btClear.grid(row=0, column=3, padx=10)
    # import csv code button
    import_csv_button = ttk.Button(btFrame, text="Import CSV Data", command=import_csv_file)
    import_csv_button.grid(row=0, column=4, padx=10)

    #
    def refresh_data():
        # Clear the current data in the Treeview
        tv.delete(*tv.get_children())

        # Fetch and display the latest data from the database
        displayAll()

    # Establish a connection to the SQLite database (replace 'Employee.db' with your database file)
    conn = sqlite3.connect('Employee.db')

    # SQL query to fetch time series data
    Timeseries_query = "SELECT employee_id, time_in_stamp, time_out_stamp, year, month, day FROM Timeseries"

    # Read the data into a DataFrame
    df_Timeseries = pd.read_sql_query(Timeseries_query, conn)

    # Function to parse custom time format
    def custom_time_parser(time_str):
        # Split the time string to separate hours, minutes, and AM/PM
        time_parts = time_str.split(':')
        hours = int(time_parts[0])
        minutes = int(time_parts[1])

        # Check if it's AM or PM and adjust the hours accordingly
        if "PM" in time_str:
            hours += 12

        # Create a datetime object with fixed seconds and microseconds
        return pd.Timestamp(year=2000, month=1, day=1, hour=hours, minute=minutes, second=0, microsecond=0)

    # Use the custom parser to convert time columns
    df_Timeseries['time_in_stamp'] = df_Timeseries['time_in_stamp'].apply(custom_time_parser)
    df_Timeseries['time_out_stamp'] = df_Timeseries['time_out_stamp'].apply(custom_time_parser)

    # Define the time ranges
    normal_start = pd.Timestamp(year=2000, month=1, day=1, hour=8, minute=0, second=0, microsecond=0)
    pd.Timestamp(year=2000, month=1, day=1, hour=16, minute=0, second=0, microsecond=0)

    # Calculate work duration per employee per day
    df_Timeseries['work_duration'] = df_Timeseries['time_out_stamp'] - df_Timeseries['time_in_stamp']

    # Calculate total work hours per employee per day in seconds
    df_Timeseries['total_work_hours'] = df_Timeseries['work_duration'].dt.total_seconds() / 3600  # Convert to hours

    # Create a DataFrame to track employees who worked overtime (over 8 hours), worked less than 8 hours, and arrived early
    df_work_status = df_Timeseries.groupby(['employee_id', 'year', 'month', 'day']).agg(
        total_work_hours=('total_work_hours', 'sum'),
        early_arrival=('time_in_stamp', lambda x: any(x <= normal_start)),
    ).reset_index()

    # Create the main Tkinter window

    # Create a frame to contain the button and Combobox

    # Create the "Track Employee Timings" button
    def display_chart_plot(event=None):
        selected_employee = employee_var.get()

        if selected_employee == "All Employees":
            data_to_plot = df_work_status
        else:
            data_to_plot = df_work_status[df_work_status['employee_id'] == int(selected_employee)]

        # Create a new Toplevel window
        chart_window = tk.Toplevel(root)
        chart_window.title("Employee Work Hours Chart")
        chart_window.geometry("1200x800")
        # Create a frame to contain the canvas
        chart_frame = ttk.Frame(chart_window)
        chart_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Use fill and expand to fill the available space
         # Set the

        # Create a Figure to hold the plot
        fig = Figure(figsize=(12, 8))

        # Add a subplot to the Figure
        ax = fig.add_subplot(111)

        # Define color coding based on conditions
        colors = []
        labels = []
        for _, row in data_to_plot.iterrows():
            if 0 <= row['total_work_hours'] <= 8:
                colors.extend(['green', 'orange', 'red', 'blue'])
                labels.extend(['0-8 hours', 'Overtime', 'Less than 8 hours', 'Early Arrival'])
            elif row['total_work_hours'] > 8:
                colors.extend(['green', 'orange', 'red', 'blue'])
                labels.extend(['0-8 hours', 'Overtime', 'Less than 8 hours', 'Early Arrival'])
            elif row['early_arrival']:
                colors.extend(['blue', 'green', 'red', 'orange'])
                labels.extend(['Early Arrival', '0-8 hours', 'Less than 8 hours', 'Overtime'])
            else:
                colors.extend(['red', 'green', 'blue', 'orange'])
                labels.extend(['Less than 8 hours', '0-8 hours', 'Early Arrival', 'Overtime'])

        # Create grouped bars
        ax.bar(data_to_plot.index, data_to_plot['total_work_hours'], color=colors)
        ax.set_xlabel('Employee and Date Index')
        ax.set_ylabel('Total Work Hours')
        ax.set_title('Employee Work Hours (Grouped Bar)')
        ax.set_xticks(data_to_plot.index)
        ax.set_xticklabels([f"Emp {row['employee_id']}, {row['year']}-{row['month']}-{row['day']}" for _, row in
                            data_to_plot.iterrows()], rotation=90)
        ax.legend(
            handles=[plt.Line2D([0], [0], color=color, lw=4, label=label) for color, label in zip(colors, labels)])

        # Create a canvas to display the Figure
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.get_tk_widget().pack()
        # Create a scrollbar for the canvas
        canvas_scrollbar = ttk.Scrollbar(chart_frame, orient="vertical", command=canvas.get_tk_widget().yview)
        canvas_scrollbar.pack(side="right", fill="y")
        canvas.get_tk_widget().configure(yscrollcommand=canvas_scrollbar.set)

    lbtlabel = ttk.Label(entries_frame, text="Track employee time")
    lbtlabel.place(x=1400, y=300)

    # Create a Combobox (dropdown) for employee selection
    employee_var = tk.StringVar()
    employee_combobox = ttk.Combobox(entries_frame, textvariable=employee_var, width=27,
                                     values=["All Employees"] + df_work_status['employee_id'].unique().tolist())
    employee_combobox.place(x=1400, y=350)

    # Bind the Combobox selection to display the chart
    employee_combobox.bind("<<ComboboxSelected>>", display_chart_plot)

    # Close the database connection
    conn.close()

    # Start the main Tkinter event loop

    # Start the main Tkinter event loop

    # Start the Tkinter main loop

    refresh_button = ttk.Button(btFrame, text="Refresh Data", command=refresh_data)
    refresh_button.grid(row=0, column=5, padx=30, pady=10)
    refresh_button.config(command=refresh_data)

    # tabel formation frame
    # Create a frame for the Treeview using grid
    tree_frame = tk.Frame(root)
    tree_frame.grid(row=8, column=0, sticky="nsew")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1, minsize=1500)

    # Rest of your Treeview and styling configuration

    # Create a style for the Treeview headings and rows
    style = ttk.Style()
    style.configure("mystyle.Treeview.Heading", background="red", font=('Arial', 15))
    style.configure("mystyle.Treeview", font=('Arial', 13), rowheight=50)

    # Create the Treeview widget with the configured style
    tv = ttk.Treeview(tree_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), style="mystyle.Treeview")

    tv.heading("1", text="ID", anchor="center")
    tv.column("1", width=5, anchor="center")

    tv.heading("2", text="NAME", anchor="center")
    tv.column("2", width=10, anchor="center")

    tv.heading("3", text="AGE", anchor="center")
    tv.column("3", width=5, anchor="center")

    tv.heading("4", text="GENDER", anchor="center")
    tv.column("4", width=10, anchor="center")

    tv.heading("5", text="EMAIL", anchor="center")
    tv.column("5", width=10, anchor="center")

    tv.heading("6", text="D.O.J", anchor="center")
    tv.column("6", width=10, anchor="center")

    tv.heading("7", text="CONTACT", anchor="center")
    tv.column("7", width=10, anchor="center")

    tv.heading("8", text="ADDRESS", anchor="center")
    tv.column("8", width=10, anchor="center")

    tv.heading("9", text="USERNAME", anchor="center")
    tv.column("9", width=10, anchor="center")

    tv.heading("10", text="PASSWORD", anchor="center")
    tv.column("10", width=10, anchor="center")

    tv['show'] = 'headings'
    tv.grid(row=0, column=0, sticky="nsew")
    tv.bind("<ButtonRelease-1>", getData)
    tv.pack(fill="x")

    displayAll()


login_window = tk.Toplevel(root)  # Create a Toplevel window for login
login_window.title("Login")
login_window.config(bg="peach puff")
login_window.state("zoomed")
# Create labels and entry widgets for username and password in the login window
login_label = tk.Label(login_window, text="LOGIN", font=("Arial black ", 22), bg="peach puff")
login_label.pack(pady=20)
login_label = tk.Label(login_window, text="EMPLOYEE MANAGEMENT SYSTEM", font=("impact", 20), bg="peach puff")
login_label.pack(pady=20)
username_label = tk.Label(login_window, text="USERNAME", bg="peach puff", font=('segoe print', 14))
username_label.pack()
username_var = tk.StringVar()
username_entry = tk.Entry(login_window, textvariable=username_var, width=30)
username_entry.pack()

password_label = tk.Label(login_window, text="PASSWORD", bg="peach puff", font=("segoe print", 14))
password_label.pack()
password_var = tk.StringVar()
password_entry = tk.Entry(login_window, textvariable=password_var, show="*", width=30)
password_entry.pack()

login_button = tk.Button(login_window, text="Login", command=validate_login, width=30)
login_button.pack(pady=20)

# Hide the main program window initially
root.withdraw()

open_main_program()

root.mainloop()
