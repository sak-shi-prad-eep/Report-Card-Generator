-- Create the database
CREATE DATABASE IF NOT EXISTS testdb;

-- Use the database
USE testdb;

-- Create login table
CREATE TABLE IF NOT EXISTS login (
    Username VARCHAR(50) PRIMARY KEY,
    Password VARCHAR(50) NOT NULL,
    Designation VARCHAR(20) NOT NULL
);

-- Create admin table (for student information)
CREATE TABLE IF NOT EXISTS admin (
    RollNo VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- Create subjects table
CREATE TABLE IF NOT EXISTS subjects (
    SubjectID VARCHAR(20) PRIMARY KEY,
    SubjectName VARCHAR(100) NOT NULL
);

-- Create marks table
CREATE TABLE IF NOT EXISTS marks (
    RollNo VARCHAR(20),
    SubjectID VARCHAR(20),
    Marks INT,
    PRIMARY KEY (RollNo, SubjectID),
    FOREIGN KEY (RollNo) REFERENCES admin(RollNo),
    FOREIGN KEY (SubjectID) REFERENCES subjects(SubjectID)
);

-- Insert some sample data
INSERT INTO login (Username, Password, Designation) VALUES
('admin', 'admin123', 'admin'),
('teacher', 'teacher123', 'teacher');

INSERT INTO admin (RollNo, Name) VALUES
('101', 'John Doe'),
('102', 'Jane Smith');

INSERT INTO subjects (SubjectID, SubjectName) VALUES
('MATH101', 'Mathematics'),
('ENG101', 'English');

INSERT INTO marks (RollNo, SubjectID, Marks) VALUES
('101', 'MATH101', 85),
('101', 'ENG101', 78),
('102', 'MATH101', 92),
('102', 'ENG101', 88);