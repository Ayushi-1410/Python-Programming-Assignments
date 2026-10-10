import csv
import mysql.connector

connection = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=input("Enter MySQL password: "),
        database="college_db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INT PRIMARY KEY,
            name VARCHAR(100),
            spi DECIMAL(3,1)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id INT,
            course_id VARCHAR(30),
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id)
                REFERENCES Student(student_id)
        )
    """)

    with open("student.csv", newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            cursor.execute("""
                INSERT INTO Student VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), spi = VALUES(spi)
            """, (row["student_id"], row["name"], row["spi"]))

    with open("registration.csv", newline="", encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            cursor.execute("""
                INSERT IGNORE INTO CourseRegistration
                VALUES (%s, %s)
            """, (row["student_id"], row["course_id"]))

    connection.commit()

    course_id = input("Enter course ID: ")
    threshold = float(input("Enter minimum SPI: "))

    cursor.execute("""
        SELECT s.student_id, s.name, s.spi, r.course_id
        FROM Student s
        JOIN CourseRegistration r
        ON s.student_id = r.student_id
        WHERE r.course_id = %s AND s.spi > %s
        ORDER BY s.spi DESC, s.student_id ASC
    """, (course_id, threshold))

    for row in cursor.fetchall():
        print(row[0], row[1], float(row[2]), row[3])

    cursor.close()

except (mysql.connector.Error, OSError, ValueError, KeyError) as error:
    print("Error:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()