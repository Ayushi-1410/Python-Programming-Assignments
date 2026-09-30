import os
import pickle
import zipfile
import re


def build_index():

    folder = input("Enter folder path: ")
    output = input("Enter ZIP file name: ")

    index = {}
    total_files = 0
    total_lines = 0

    if not os.path.exists(folder):
        print("Folder not found")
        return

    for filename in os.listdir(folder):

        if not filename.endswith(".txt"):
            continue

        total_files += 1

        path = os.path.join(folder, filename)

        with open(path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, 1):

                total_lines += 1

                words = re.findall(
                    r"\b\w+\b",
                    line.lower()
                )

                for word in words:

                    if word not in index:
                        index[word] = []

                    index[word].append(
                        (filename, line_number)
                    )

    data = {
        "files": total_files,
        "lines": total_lines,
        "index": index
    }

    pickle_file = "log_index.pkl"

    with open(pickle_file, "wb") as file:
        pickle.dump(data, file)

    with zipfile.ZipFile(
        output,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        zip_file.write(pickle_file)

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search_index():

    pickle_path = input("Enter pickle file path: ")
    query = input("Enter search words: ").split()

    try:

        with open(pickle_path, "rb") as file:
            data = pickle.load(file)

    except:
        print("File not found")
        return

    index = data["index"]

    for word in query:

        word = word.lower()

        if word in index:

            print(word + ":", end=" ")

            for filename, line in index[word]:
                print(
                    filename + ":" + str(line),
                    end=" "
                )

            print()

        else:
            print(word + ": Not Found")


print("COMPRESSED LOG INDEX")
print("1. BUILD")
print("2. SEARCH")

choice = input("Enter your choice: ")

if choice == "1":

    build_index()

elif choice == "2":

    search_index()

else:

    print("Invalid choice")