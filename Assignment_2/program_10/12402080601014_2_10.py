import csv
import os
import matplotlib.pyplot as plt

input_file = input("Enter CSV file path: ")
output_folder = input("Enter output folder: ")

os.makedirs(output_folder, exist_ok=True)

subjects = ["Python", "DBMS", "OS"]
students = []
subject_marks = {subject: [] for subject in subjects}

with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        student = {
            "enrollment": row["enrollment"],
            "name": row["name"]
        }

        for subject in subjects:
            try:
                mark = float(row[subject])
                if not 0 <= mark <= 100:
                    mark = None
            except (ValueError, TypeError):
                mark = None

            student[subject] = mark

            if mark is not None:
                subject_marks[subject].append(mark)

        students.append(student)

with open(os.path.join(output_folder, "cleaned_marks.csv"),
          "w", newline="", encoding="utf-8") as file:
    columns = ["enrollment", "name"] + subjects
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(students)

with open(os.path.join(output_folder, "summary.csv"),
          "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Subject", "Count", "Average"])

    for subject in subjects:
        marks = subject_marks[subject]
        average = sum(marks) / len(marks) if marks else 0
        writer.writerow([subject, len(marks), round(average, 2)])

names = []
averages = []

for student in students:
    marks = [
        student[s] for s in subjects
        if student[s] is not None
    ]

    if marks:
        names.append(student["name"])
        averages.append(sum(marks) / len(marks))

plt.figure()
plt.hist(averages, bins=5)
plt.title("Grade Distribution")
plt.xlabel("Average Marks")
plt.ylabel("Students")
plt.savefig(os.path.join(output_folder, "grade_distribution.png"))
plt.close()

subject_averages = [
    sum(subject_marks[s]) / len(subject_marks[s])
    if subject_marks[s] else 0
    for s in subjects
]

plt.figure()
plt.bar(subjects, subject_averages)
plt.title("Subject Average")
plt.ylabel("Average Marks")
plt.savefig(os.path.join(output_folder, "subject_average.png"))
plt.close()

ranked = sorted(
    zip(names, averages),
    key=lambda x: (-x[1], x[0].lower())
)[:5]

plt.figure()
plt.bar([x[0] for x in ranked], [x[1] for x in ranked])
plt.title("Top Performers")
plt.ylabel("Average Marks")
plt.savefig(os.path.join(output_folder, "top_performers.png"))
plt.close()

print("All files created successfully.")