import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
normal_end = pd.Timestamp(year=2000, month=1, day=1, hour=16, minute=0, second=0, microsecond=0)

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
root = tk.Tk()
root.title("Employee Work Hours Chart")

# Create a frame to contain the button and Combobox
control_frame = ttk.Frame(root)
control_frame.pack(padx=10, pady=10)


# Create the "Track Employee Timings" button
def display_chart_plot(event):
    selected_employee = employee_var.get()

    if selected_employee == "All Employees":
        data_to_plot = df_work_status
    else:
        data_to_plot = df_work_status[df_work_status['employee_id'] == int(selected_employee)]

    # Create a new Toplevel window
    chart_window = tk.Toplevel(root)
    chart_window.title("Employee Work Hours Chart")

    # Create a frame to contain the canvas
    chart_frame = ttk.Frame(chart_window)
    chart_frame.pack(padx=10, pady=10)

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


# Create a Combobox (dropdown) for employee selection
employee_var = tk.StringVar()
employee_combobox = ttk.Combobox(control_frame, textvariable=employee_var,
                                 values=["All Employees"] + df_work_status['employee_id'].unique().tolist())
employee_combobox.grid(row=1, column=0, columnspan=2)

# Bind the Combobox selection to display the chart
employee_combobox.bind("<<ComboboxSelected>>", display_chart_plot)

# Close the database connection
conn.close()

# Start the main Tkinter event loop
root.mainloop()
