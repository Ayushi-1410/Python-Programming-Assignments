import re

expressions = {}

memo = {}

visiting = set()

def calculate(variable):

    if variable in memo:
        return memo[variable]

    if variable in visiting:
        raise ValueError("CYCLE")

    if variable not in expressions:
        raise ValueError("INVALID")

    visiting.add(variable)

    expression = expressions[variable]

    variables = re.findall(r'[A-Za-z_][A-Za-z0-9_]*', expression)

    values = {}

    for name in variables:

        if name not in expressions:
            raise ValueError("INVALID")

        values[name] = calculate(name)

    try:
 
        result = eval(
            expression,
            {"__builtins__": {}},
            values
        )

    except:
        raise ValueError("INVALID")

    visiting.remove(variable)

    memo[variable] = result

    return result

print("==========================================")
print("     RECURSIVE EXPRESSION ENGINE")
print("==========================================")

print("\nEnter number of variables:")
v = int(input())

print("\nEnter variable definitions:")
print("Example: a = 2 + 3")

for i in range(v):

    line = input().strip()

    if "=" not in line:
        continue

    variable, expression = line.split("=", 1)

    variable = variable.strip()
    expression = expression.strip()

    expressions[variable] = expression

print("\nEnter expression to evaluate:")

target = input().strip()

try:

    target_variables = re.findall(
        r'[A-Za-z_][A-Za-z0-9_]*',
        target
    )

    values = {}

    for name in target_variables:

        if name not in expressions:
            raise ValueError("INVALID")

        values[name] = calculate(name)

    answer = eval(
        target,
        {"__builtins__": {}},
        values
    )

    print("\nOutput:", answer)

except ValueError as error:

    if str(error) == "CYCLE":
        print("\nOutput: CYCLE")

    else:
        print("\nOutput: INVALID")

except:

    print("\nOutput: INVALID")