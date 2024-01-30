SELECT 'CREATE DATABASE test' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test')\gexec

\c test;

-- Create the student table without "marks" and "grade"
CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    phone_number VARCHAR(15)
);

-- Create the marks table with foreign key reference to the student table
CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(student_id),
    subject VARCHAR(50),
    marks INT
);

-- Insert values into the student table
INSERT INTO student (first_name, last_name, age, phone_number)
VALUES
    ('John', 'Doe', 20, '+1234567890'),
    ('Jane', 'Smith', 22, '+1987654321'),
    ('Alice', 'Johnson', 21, '+1654321897'),
    ('Bob', 'Williams', 23, '+1789456123'),
    ('Emily', 'Davis', 19, '+1543219876'),
    ('Michael', 'Brown', 24, '+1876543210'),
    ('Sophia', 'Miller', 20, '+1987654321'),
    ('Daniel', 'Jones', 22, '+1765432109'),
    ('Olivia', 'Taylor', 21, '+1928374650'),
    ('William', 'Moore', 23, '+1345678901');

-- Insert values into the marks table
INSERT INTO marks (student_id, subject, marks)
VALUES
    (1, 'Math', 95),
    (1, 'History', 90),
    (2, 'Math', 85),
    (2, 'History', 88),
    (3, 'Math', 92),
    (3, 'History', 94),
    (4, 'Math', 78),
    (4, 'History', 80),
    (5, 'Math', 88),
    (5, 'History', 85);

