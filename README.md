# employee_datas_program
 
![Picture1](https://github.com/ajithcap/project/assets/104433561/3e11604a-94ab-4398-9494-a1b9c7108e88)

# Employee Management System

The Employee Management System is a Python application built using the Tkinter library for the graphical user interface. This program helps manage employee records, track their work hours, and perform various operations such as adding, updating, and deleting employee data.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

### 1. Employee Record Management

- Add new employee records with details such as name, age, gender, email, date of joining, contact information, username, and password.
- Update existing employee records.
- Delete employee records.
- Clear input fields.
- Import employee data from a CSV file.

### 2. Work Time Tracking

- Track and analyze employees' work hours.
- Calculate and display work duration.
- Identify employees who worked overtime (more than 8 hours) or arrived early.
- Generate a grouped bar chart to visualize work hours.

### 3. Customized Welcome Page

- A customized welcome page where employees can log in and enter their time-in and time-out information.

### 4. User Authentication

- Secure login system with user authentication using usernames and passwords.

### 5. Database Integration

- Store employee data and time tracking information in an SQLite database.
- Perform database operations using the provided `db` module.

## Getting Started

To run the Employee Management System on your local machine, follow these steps:

### Prerequisites

- Python 3.x installed on your system.
- Required Python packages (dependencies) installed. You can install them using `pip`:

```bash
pip install pillow matplotlib pandas tkcalendar
Usage
Launch the application by running main.py.
Use the menu to navigate through the program's functionalities:
Employee Records: Add, update, delete, or import employee records.
Work Time Tracking: Analyze work hours and view the work hours chart.
Customized Welcome Page: Log in and enter time-in and time-out information.
Follow the on-screen instructions to perform the desired operations.
Contributing
Contributions are welcome! If you have suggestions, improvements, or bug fixes, please open an issue or create a pull request.
