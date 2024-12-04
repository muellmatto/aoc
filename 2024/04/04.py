testcase = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

testcase_result = 18
testcase_b_result = 9


def get_letter(puzzle, x, y):
    lines = puzzle.splitlines()
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1
    if x > max_x or y > max_y or x < 0 or y < 0:
        return None
    line = lines[y]
    letter = line[x]
    return letter


def find_xmas_at(puzzle, x, y, direction):
    dx, dy = 0, 0
    if "n" in direction:
        dy = -1
    if "s" in direction:
        dy = 1
    if "e" in direction:
        dx = 1
    if "w" in direction:
        dx = -1
    for letter in "XMAS":
        if get_letter(puzzle, x, y) == letter:
            x += dx
            y += dy
        else:
            return False
    return True


def count_xmas(puzzle):
    directions = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]
    result = 0
    lines = puzzle.splitlines()
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            for direction in directions:
                if find_xmas_at(puzzle, x, y, direction):
                    result += 1
    return result


def find_X_MAS_at(puzzle, x, y):
    if get_letter(puzzle, x, y) == "A":
        if (  # diagonal-MAS /
            (
                get_letter(puzzle, x + 1, y + 1) == "S"
                and get_letter(puzzle, x - 1, y - 1) == "M"
            )
            or (
                get_letter(puzzle, x + 1, y + 1) == "M"
                and get_letter(puzzle, x - 1, y - 1) == "S"
            )
        ) and (
            (  # diagonal-MAS \
                get_letter(puzzle, x + 1, y - 1) == "S"
                and get_letter(puzzle, x - 1, y + 1) == "M"
            )
            or (
                get_letter(puzzle, x + 1, y - 1) == "M"
                and get_letter(puzzle, x - 1, y + 1) == "S"
            )
        ):
            return True

    return False


def count_x_mas(puzzle):
    result = 0
    lines = puzzle.splitlines()
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if find_X_MAS_at(puzzle, x, y):
                result += 1
    return result


# print(count_xmas(testcase))
# print(count_x_mas(testcase))

with open("input.txt", "r") as f:
    data = f.read()

print(count_xmas(data))
print(count_x_mas(data))
