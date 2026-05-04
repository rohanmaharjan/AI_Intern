import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("Database_Password")
)

cursor = conn.cursor()

# Create database and use it
cursor.execute("CREATE DATABASE IF NOT EXISTS grades")
cursor.execute("USE grades")

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS students")

# Create students table
cursor.execute("""
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    subject VARCHAR(50) NOT NULL,
    score FLOAT NOT NULL,
    grade VARCHAR(2)
)
""")

# Function to assign grade
def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

# Student data (15 students)
students_list = [
    ("Ram", "Math", 73),
    ("Sita", "Science", 95),
    ("Bhavana", "English", 41),
    ("Harry", "History", 88),
    ("Gopal", "Math", 67),
    ("Salman", "Science", 54),
    ("Gita", "English", 92),
    ("Grishma", "History", 36),
    ("Shyam", "Math", 100),
    ("Chadani", "Science", 79),
    ("Kevin", "English", 62),
    ("Sumit", "History", 47),
    ("Roj", "Math", 85),
    ("Bina", "Science", 28),
    ("Tina", "English", 90)
]

# Insert students with duplicate name check
for student in students_list:
    name, subject, score = student

    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE name = %s",
        (name,)
    )

    exists = cursor.fetchone()[0]

    if exists == 0:
        cursor.execute(
            "INSERT INTO students (name, subject, score) VALUES (%s, %s, %s)",
            (name, subject, score)
        )
    else:
        print(f"Student '{name}' already exists. Skipping insert.")

conn.commit()

# Update grade column using assign_grade()
cursor.execute("SELECT id, score FROM students")

for student_id, score in cursor.fetchall():
    grade = assign_grade(score)

    cursor.execute(
        "UPDATE students SET grade = %s WHERE id = %s",
        (grade, student_id)
    )

conn.commit()

# Delete students who scored below 50
cursor.execute("DELETE FROM students WHERE score < 50")
conn.commit()

# Add new column: passed
cursor.execute("""
ALTER TABLE students
ADD COLUMN passed BOOLEAN
""")

# Set passed = TRUE if score >= 50 else FALSE
cursor.execute("""
UPDATE students
SET passed = (score >= 50)
""")

conn.commit()

# Query: count of students per grade ordered from A to F
print("\nCount of students per grade:\n")

cursor.execute("""
SELECT grade, COUNT(*)
FROM students
GROUP BY grade
ORDER BY FIELD(grade, 'A', 'B', 'C', 'D', 'F')
""")

for grade, count in cursor.fetchall():
    print(f"Grade {grade}: {count} students")

# Display final student records
print("\nFinal Student Records:\n")

cursor.execute("""
SELECT id, name, subject, score, grade, passed
FROM students
""")

for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()

print("\nDatabase operation completed successfully.")