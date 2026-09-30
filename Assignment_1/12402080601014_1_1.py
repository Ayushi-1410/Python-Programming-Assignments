
print("==========================================")
print("       CAMPUS MERIT ANALYZER")
print("==========================================")


print("\nEnter number of students, Top K students and number of subjects:")
n, k, m = map(int, input().split())


students = {}

print("\nEnter student details:")
print("Format: Enrollment Name Semester CPI Subject1 Subject2 ...")

for i in range(n):

    print("\nEnter details of student", i + 1, ":")

    data = input().split()

    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])

    marks = []

    for j in range(m):
        marks.append(int(data[4 + j]))

    student = {
        "enrollment": enrollment,
        "name": name,
        "semester": semester,
        "cpi": cpi,
        "marks": marks
    }

    if semester not in students:
        students[semester] = []

    students[semester].append(student)

print("\n==========================================")
print("              RESULT")
print("==========================================")

for semester in sorted(students.keys()):

    student_list = students[semester]

    for student in student_list:

        total_marks = sum(student["marks"])
        average_marks = total_marks / m

        student["average"] = average_marks

    student_list.sort(
        key=lambda student: (
            -student["cpi"],
            -student["average"],
            student["enrollment"]
        )
    )

    print("\nSemester", semester, ":", end=" ")

    top_students = min(k, len(student_list))

    for i in range(top_students):
        print(student_list[i]["enrollment"], end=" ")

    print()

    for subject in range(m):

        highest_marks = -1
        toppers = []

        for student in student_list:

            mark = student["marks"][subject]

            if mark > highest_marks:

                highest_marks = mark

                toppers = [student["enrollment"]]

            elif mark == highest_marks:

                toppers.append(student["enrollment"])
        toppers.sort()

        print("S" + str(subject + 1) + ":", end=" ")

        for enrollment in toppers:
            print(enrollment, end=" ")

        print()