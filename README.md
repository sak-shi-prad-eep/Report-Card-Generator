# Report Card System

## Overview
This Report Card System is a comprehensive desktop application built with Python and Tkinter. It provides a user-friendly interface for managing student grades, allowing different levels of access for administrators, teachers, and students. The system uses MySQL for data storage and retrieval.

## Features

### User Roles
- **Admin**: Can insert, update, delete, and view student records.
- **Teacher**: Can insert, update, and view marks for their specific subject.
- **Student**: Can view their own report card.

### Functionality
- **Login System**: Secure login for different user roles.
- **Admin Panel**: Manage student records (CRUD operations).
- **Teacher Panel**: Manage marks for a specific subject.
- **Student Panel**: View individual report cards.
- **Password Reset**: Option to reset passwords for users.

## Technical Details

### Dependencies
- Python 3.x
- Tkinter
- MySQL Connector for Python

### Database Structure
The application uses a MySQL database with the following tables:
- `login`: Stores user credentials and roles
- `admin`: Stores student information
- `marks`: Stores student marks for each subject
- `subjects`: Stores subject information

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/report-card-system.git
   ```

2. Install required dependencies:
   ```
   pip install mysql-connector-python
   ```

3. Set up your MySQL database and update the connection details in the `connect_db()` function.

4. Run the application:
   ```
   python main.py
   ```

## Usage

1. **Login**: 
   - Use appropriate credentials for Admin, Teacher, or Student access.

2. **Admin Functions**:
   - Insert new student records
   - Update existing student information
   - Delete student records
   - View all student records

3. **Teacher Functions**:
   - Enter subject ID
   - Insert marks for students
   - Update existing marks
   - View marks for their subject

4. **Student Functions**:
   - Enter roll number to view report card
   - Option to print report card

## Security Considerations

- Passwords are stored in plain text in the current implementation. For a production environment, implement proper password hashing.
- The database connection uses a hardcoded password. In a real-world scenario, use environment variables or a configuration file to store sensitive information.

## Future Enhancements

- Implement data validation and error handling
- Add data export functionality (e.g., to CSV or PDF)
- Implement a more sophisticated authentication system
- Create a web-based version of the application
