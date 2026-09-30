class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


variables = {}

print("INTERACTIVE FORMULA VALIDATOR")
print("Enter 'quit' to stop")

while True:

    line = input("Enter formula: ")

    if line == "quit":
        break

    try:

        if "%" in line:
            raise UnsupportedOperatorError()

        if "=" in line:

            parts = line.split("=", 1)

            name = parts[0].strip()
            expression = parts[1].strip()

            if not name.isidentifier():
                raise ValueError()

            result = eval(
                expression,
                {"__builtins__": {}},
                variables
            )

            variables[name] = result

            print("Result:", result)

        else:

            if "/" in line:

                parts = line.split("/")

                for part in parts[1:]:

                    value = eval(
                        part,
                        {"__builtins__": {}},
                        variables
                    )

                    if value == 0:
                        raise DivisionByZeroError()

            result = eval(
                line,
                {"__builtins__": {}},
                variables
            )

            print("Result:", result)

    except DivisionByZeroError:
        print("DivisionByZeroError")

    except UnsupportedOperatorError:
        print("UnsupportedOperatorError")

    except NameError:
        print("UnknownVariableError")

    except:
        print("InvalidFormulaError")