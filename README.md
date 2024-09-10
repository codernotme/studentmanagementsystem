# Student Management System

## Overview

The Student Management System is a desktop application developed using Python's `tkinter` for the graphical user interface and `pymysql` for database interactions. This system allows users to add, view, search, update, and delete student records. It interfaces with a MySQL database to manage student data efficiently.

## Features

- **Add New Student**: Form to input student details and save them to the database.
- **View Students**: Display a list of all students in a scrollable table format.
- **Search Student**: Search for a student by roll number and display their details.
- **Update Student**: Update the details of a student by roll number.
- **Delete Student**: Remove a student record from the database by roll number.

## Installation

### Prerequisites

- Python 3.x
- MySQL Server
- `pymysql` package (for MySQL database interaction)
- `tkinter` package (for the GUI, included with Python standard library)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/codernotme/studentmanagementsystem.git
   cd studentmanagementsystem
   ```

2. **Install dependencies:**
   ```bash
   pip install pymysql
   ```

3. **Set up the database:**

   Run the following SQL commands in your MySQL server to create the database and table:

   ```sql
   CREATE DATABASE IF NOT EXISTS student_db;
   USE student_db;
   CREATE TABLE IF NOT EXISTS students (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       father VARCHAR(100) NOT NULL,
       class VARCHAR(20) NOT NULL,
       roll_no VARCHAR(20) UNIQUE NOT NULL,
       sex ENUM('M', 'F', 'T') NOT NULL,
       phone VARCHAR(15) NOT NULL
   );
   ```

4. **Configure Database Connection:**

   Update the `get_db_connection()` function in the `StudentManagementApp` class with your MySQL server credentials:

   ```python
   def get_db_connection():
       return pymysql.connect(
           host='localhost',
           user='root',
           password='yourpassword',  # Replace with your MySQL password
           database='student_db'
       )
   ```

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Application Interface:**
   - **Add New Student**: Opens a form to input student details.
   - **View Students**: Shows all student records in a scrollable table.
   - **Search Student**: Allows searching by roll number.
   - **Update Student**: Allows updating student details by roll number.
   - **Delete Student**: Allows deletion of student records by roll number.

## Code Structure

- `app.py`: Main application file containing the GUI and database logic.
- `database.sql`: SQL script to set up the database and table.

## Contributing

Feel free to fork the repository and submit pull requests. For bug reports and feature requests, please open an issue on the GitHub repository page.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---------

Just replace placeholders like `yourusername` and `yourpassword` with your actual values.
