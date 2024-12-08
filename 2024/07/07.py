testcase = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

testresult = 3

# ------------

with open("input", "r") as f:
    puzzle = f.read()


def equation_could_be_true(equation, part_2=False):
    solution, numbers = equation.split(": ")
    solution = int(solution)
    numbers = [int(n) for n in numbers.split(" ")]
    possible_combinations = []

    def try_operators(numbers, result=None, calculation=""):
        if len(numbers) == 0:
            possible_combinations.append((result, calculation))
        else:
            value, numbers = numbers[0], numbers[1:]
            if result == None:
                result = value
                calculation += str(value)
                try_operators(numbers, result, calculation)
            else:
                try_operators(numbers, result + value, calculation + f"+{value}")
                try_operators(numbers, result * value, calculation + f"*{value}")
                if part_2:
                    result = int(str(result) + str(value))
                    try_operators(numbers, result, calculation + f"{value}")

    try_operators(numbers=numbers)
    for result, calculation in possible_combinations:
        if result == solution:
            # print(f"\t{calculation}={solution}")
            return True, solution
    return False, -1


# puzzle = testcase

total_calibration_result = 0
for equation in puzzle.splitlines():
    solvable, result = equation_could_be_true(equation, part_2=True)
    if solvable:
        total_calibration_result += result
print(total_calibration_result)
