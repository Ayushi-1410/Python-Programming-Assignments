class BankError(Exception):
    pass

class Account:

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):

        if amount <= 0:
            raise BankError("Invalid amount")

        self.balance += amount

    def withdraw(self, amount):

        if amount <= 0:
            raise BankError("Invalid amount")

        if self.balance < amount:
            raise BankError("Insufficient balance")

        self.balance -= amount

class Transaction:

    def __init__(self, operation):
        self.operation = operation

    def execute(self, bank):

        data = self.operation.split()

        command = data[0]

        if command == "DEPOSIT":

            account_id = data[1]
            amount = int(data[2])

            if account_id not in bank.accounts:
                raise BankError("Account not found")

            bank.accounts[account_id].deposit(amount)

        elif command == "WITHDRAW":

            account_id = data[1]
            amount = int(data[2])

            if account_id not in bank.accounts:
                raise BankError("Account not found")

            bank.accounts[account_id].withdraw(amount)

        elif command == "TRANSFER":

            from_account = data[1]
            to_account = data[2]
            amount = int(data[3])

            if from_account not in bank.accounts:
                raise BankError("Account not found")

            if to_account not in bank.accounts:
                raise BankError("Account not found")

            bank.accounts[from_account].withdraw(amount)

            bank.accounts[to_account].deposit(amount)


        else:
            raise BankError("Invalid operation")

class Bank:

    def __init__(self):
        self.accounts = {}

    def add_account(self, account_id, balance):

        self.accounts[account_id] = Account(
            account_id,
            balance
        )

    def save_balances(self):

        saved = {}

        for account_id in self.accounts:
            saved[account_id] = self.accounts[account_id].balance

        return saved

    def restore_balances(self, saved):

        for account_id in saved:
            self.accounts[account_id].balance = saved[account_id]


print("==========================================")
print("       BANK SETTLEMENT SYSTEM")
print("==========================================")

n = int(input("Enter number of accounts: "))

bank = Bank()

print("\nEnter account details:")

for i in range(n):

    data = input().split()

    account_id = data[0]
    balance = int(data[1])

    bank.add_account(account_id, balance)

q = int(input("\nEnter number of operations: "))

failed_batches = []
batch_number = 0

inside_batch = False
batch_failed = False
saved_balances = None

for i in range(q):

    operation = input().strip()

    if operation == "BATCH_BEGIN":

        batch_number += 1

        inside_batch = True
        batch_failed = False

        saved_balances = bank.save_balances()

    elif operation == "BATCH_END":

        if inside_batch:

            if batch_failed:

                bank.restore_balances(saved_balances)

                failed_batches.append(batch_number)

            inside_batch = False
            batch_failed = False
            saved_balances = None

    else:

        if inside_batch and batch_failed:
            continue

        transaction = Transaction(operation)

        try:

            transaction.execute(bank)

        except BankError:

            if inside_batch:

                batch_failed = True

            else:

                pass



if len(failed_batches) > 0:

    for batch in failed_batches:
        print("FAILED", batch)

else:

    print("No batch failed")


for account_id in sorted(bank.accounts.keys()):

    account = bank.accounts[account_id]

    print(account_id, account.balance)