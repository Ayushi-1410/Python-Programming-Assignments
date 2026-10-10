import re
from collections import defaultdict

file_path = input("Enter text file path: ")

pattern = r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(?:com|edu|org)\b'

emails_by_domain = defaultdict(set)

try:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            emails = re.findall(pattern, line, re.IGNORECASE)

            for email in emails:
                email = email.lower()
                domain = email.split("@")[1]
                emails_by_domain[domain].add(email)

    for domain in sorted(emails_by_domain):
        emails = emails_by_domain[domain]
        unique_users = {email.split("@")[0] for email in emails}

        print(domain, len(unique_users), min(emails))

except FileNotFoundError:
    print("File not found. Please check the file path.")