from copy import copy
from itertools import combinations
from math import gcd

testcase = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

testresult = 14


class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        return iter((self.x, self.y))

    def __hash__(self):
        return hash(self.__repr__())

    def __mul__(self, other):
        if type(other) is int:
            return Vector(other * self.x, other * self.y)
        elif type(other) is Vector:
            raise NotImplementedError("not needed by now")
        else:
            raise TypeError("only int * Vector is implemended")

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):
        return self.__mul__(other)


class AntinodeCalculator(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        puzzle_rows = self.puzzle.splitlines()
        self.max_y = len(puzzle_rows)
        self.max_x = len(puzzle_rows[0])
        self.antinode_set = set()

    def _add_antinode(self, antenna):
        if (
            antenna.x >= 0
            and antenna.x < self.max_x
            and antenna.y >= 0
            and antenna.y < self.max_y
        ):
            self.antinode_set.add(copy(antenna))
            return True
        return False

    def find(self, character):
        positions = []
        position = 0
        while True:
            position = self.puzzle.find(character, position + 1)
            if position == -1:
                break
            y = position // (self.max_y + 1)
            x = position % (self.max_x + 1)
            positions.append(Vector(x, y))
        return positions

    def get_set_of_antenna_chars(self):
        chars_to_exclude = {".", "\n"}
        antenna_chars = set(self.puzzle) - chars_to_exclude
        return antenna_chars

    def add_antinodes_for_antennas(self, antenna_1, antenna_2):
        position_1 = 2 * antenna_1 - antenna_2
        position_2 = 2 * antenna_2 - antenna_1
        self._add_antinode(position_1)
        self._add_antinode(position_2)
        return True

    def add_antinodes_for_antennas_part2(self, antenna_1, antenna_2):
        v = antenna_2 - antenna_1
        divisor = gcd(v.x, v.y)
        x_min = int(round(v.x / divisor, 0))
        y_min = int(round(v.y / divisor, 0))
        v_min = Vector(x_min, y_min)
        k = 0
        while True:
            success = self._add_antinode(antenna_1 + k * v)
            if success:
                k += 1
            else:
                break
        k = 0
        while True:
            success = self._add_antinode(antenna_1 + k * v)
            if success:
                k -= 1
            else:
                break
        return True


with open("input", "r") as f:
    puzzle = f.read()

antinode_calculator = AntinodeCalculator(puzzle)

for char in antinode_calculator.get_set_of_antenna_chars():
    antennas = antinode_calculator.find(char)
    if len(antennas) > 1:
        for antenna_1, antenna_2 in combinations(antennas, 2):
            antinode_calculator.add_antinodes_for_antennas(antenna_1, antenna_2)

print(len(antinode_calculator.antinode_set))

# Part 2
del antinode_calculator
antinode_calculator = AntinodeCalculator(puzzle)

for char in antinode_calculator.get_set_of_antenna_chars():
    antennas = antinode_calculator.find(char)
    if len(antennas) > 1:
        for antenna_1, antenna_2 in combinations(antennas, 2):
            antinode_calculator.add_antinodes_for_antennas_part2(antenna_1, antenna_2)

print(len(antinode_calculator.antinode_set))
