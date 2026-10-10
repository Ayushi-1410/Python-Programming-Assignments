import mysql.connector

allowed_columns = {
    "student.id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.name": "c.course_name"
}

print("Allowed columns:", ", ".join(allowed_columns))

fields = input("Enter columns separated by commas: ").lower().split(",")
fields = [field.strip() for field in fields]

if not fields or any(field not in allowed_columns for field in fields):
    print("Invalid column selected.")
    raise SystemExit

course_id = input("Enter course ID or press Enter to skip: ")
min_spi = input("Enter minimum SPI or press Enter to skip: ")

try:
    limit = int(input("Enter limit (1-1000): "))
    if not 1 <= limit <= 1000:
        raise ValueError
    min_spi = float(min_spi) if min_spi else None
except ValueError:
    print("Invalid limit or SPI.")
    raise SystemExit

sql = """
SELECT {fields}
FROM Student s
JOIN CourseRegistration r ON s.student_id = r.student_id
JOIN Course c ON r.course_id = c.course_id
""".format(fields=", ".join(allowed_columns[field] for field in fields))

conditions = []
params = []

if course_id:
    conditions.append("c.course_id = %s")
    params.append(course_id)

if min_spi is not None:
    conditions.append("s.spi >= %s")
    params.append(min_spi)

if conditions:
    sql += " WHERE " + " AND ".join(conditions)

sql += " ORDER BY s.spi DESC LIMIT %s"
params.append(limit)

connection = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=input("Enter MySQL password: "),
        database="college_db"
    )

    cursor = connection.cursor()
    cursor.execute(sql, tuple(params))

    print("SQL_OK")
    for row in cursor.fetchall():
        print(*row)

    cursor.close()

except mysql.connector.Error as error:
    print("Database error:", error)

finally:
    if connection is not None and connection.is_connected():
        connection.close()