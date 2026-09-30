import csv

print("======================================")
print("     CSV TRANSACTION SPLITTER")
print("======================================")

file_name = input("Enter CSV file name: ")

credit_rows = []
debit_rows = []
error_rows = []

balances = {}

try:

    with open(file_name, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:

                transaction_id = row["tid"]
                account_id = row["account"]
                transaction_type = row["type"]
                amount = row["amount"]
                timestamp = row["time"]

                if transaction_type not in ["CREDIT", "DEBIT"]:
                    raise ValueError("Invalid transaction type")

                amount = float(amount)

                if amount <= 0:
                    raise ValueError("Amount must be greater than 0")

                if transaction_type == "CREDIT":

                    credit_rows.append(row)

                    if account_id not in balances:
                        balances[account_id] = 0

                    balances[account_id] += amount

                else:

                    debit_rows.append(row)

                    if account_id not in balances:
                        balances[account_id] = 0

                    balances[account_id] -= amount

            except Exception as error:

                row["reason"] = str(error)

                error_rows.append(row)

                continue

except FileNotFoundError:

    print("File not found!")
    exit()

with open("credit.csv", "w", newline="") as file:

    fieldnames = [
        "tid",
        "account",
        "type",
        "amount",
        "time"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for row in credit_rows:

        writer.writerow(row)

with open("debit.csv", "w", newline="") as file:

    fieldnames = [
        "tid",
        "account",
        "type",
        "amount",
        "time"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for row in debit_rows:

        writer.writerow(row)

with open("error.csv", "w", newline="") as file:

    fieldnames = [
        "tid",
        "account",
        "type",
        "amount",
        "time",
        "reason"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for row in error_rows:

        writer.writerow(row)

sorted_balances = sorted(
    balances.items(),
    key=lambda item: abs(item[1]),
    reverse=True
)

print("\n======================================")
print("          ACCOUNT BALANCES")
print("======================================")

for account, balance in sorted_balances:
    
    if balance.is_integer():
        balance = int(balance)

    print(account, balance)


print("\nFiles created:")
print("credit.csv")
print("debit.csv")
print("error.csv")