
print("==========================================")
print("       PASSWORD AUDIT SYSTEM")
print("==========================================")

print("\nEnter number of banned words:")
b = int(input())

banned_words = []

print("\nEnter banned words:")

for i in range(b):
    word = input().strip()
    banned_words.append(word)

print("\nEnter number of passwords:")
n = int(input())

print("\nEnter passwords:")

passwords = []

for i in range(n):
    password = input().strip()
    passwords.append(password)

print("\n==========================================")
print("              RESULT")
print("==========================================")

for i in range(n):

    password = passwords[i]

    if len(password) < 6 or len(password) > 12:

        print(str(i + 1) + ":", "WEAK_LENGTH")
        continue

    compromised = False

    for word in banned_words:

        if word in password:
            compromised = True
            break

    if compromised:

        print(str(i + 1) + ":", "COMPROMISED")
        continue

    has_uppercase = False

    for character in password:

        if character.isupper():
            has_uppercase = True
            break

    has_lowercase = False

    for character in password:

        if character.islower():
            has_lowercase = True
            break

    has_digit = False

    for character in password:

        if character.isdigit():
            has_digit = True
            break

    special_symbols = "$@#"

    has_special = False

    for character in password:

        if character in special_symbols:
            has_special = True
            break


    repeated = False
    count = 1

    for j in range(1, len(password)):

        if password[j] == password[j - 1]:

            count = count + 1

            if count > 3:
                repeated = True
                break

        else:

            count = 1

    if not has_uppercase or not has_lowercase or not has_digit or not has_special:

        print(str(i + 1) + ":", "WEAK_PATTERN")

    elif repeated:

        print(str(i + 1) + ":", "WEAK_PATTERN")

    else:

        print(str(i + 1) + ":", "STRONG")