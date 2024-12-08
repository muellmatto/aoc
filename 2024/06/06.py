from copy import copy

testcase = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
testresult = 41


with open("input", "r") as f:
    puzzle = f.read()

# ------


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


class Guard(object):
    def __init__(self, puzzle, extra_obstruction=None):
        self.lab = self.build_lab(puzzle)
        position, direction = self.get_initial_position_and_direction(puzzle)
        self.position = position
        self.direction = direction
        self.max_x = len(self.lab[0])
        self.max_y = len(self.lab)
        self.walk_log = []
        self.log_movement()
        self.extra_obstruction = extra_obstruction
        self.is_looping = False
        if extra_obstruction:
            x, y = extra_obstruction
            self.lab[y][x] = "#"

    def get_initial_position_and_direction(self, puzzle):
        directions = {"^": (0, -1), ">": (1, 0), "<": (-1, 0), "V": (0, 1)}
        for y, row in enumerate(self.lab):
            for guard in directions.keys():
                if guard in row:
                    direction = Vector(*directions[guard])
                    position = Vector(row.index(guard), y)
        return position, direction

    def build_lab(self, puzzle):
        return [list(row) for row in puzzle.splitlines()]

    def __repr__(self):
        return f"Guard( position={self.position}, direction={self.direction} )"

    def log_movement(self):
        position = copy(self.position)
        direction = copy(self.direction)
        self.walk_log.append((position, direction))
        return True

    def get_direction_char(self):
        if self.direction == Vector(0, -1):
            return "^"
        elif self.direction == Vector(1, 0):
            return ">"
        elif self.direction == Vector(-1, 0):
            return "<"
        elif self.direction == Vector(0, 1):
            return "V"
        else:
            return "O"

    def turn_right(self):
        origin_x = self.direction.x
        origin_y = self.direction.y
        self.direction.x = -1 * origin_y
        self.direction.y = origin_x

    def ahead(self):
        ahead_coordinates = self.position + self.direction
        if (
            ahead_coordinates.x >= 0
            and ahead_coordinates.x < self.max_x
            and ahead_coordinates.y >= 0
            and ahead_coordinates.y < self.max_y
        ):
            return self.lab[ahead_coordinates.y][ahead_coordinates.x]
        return None  # out of lab

    def get_map(self):
        lab_rows = [" " + "".join(row) for row in self.lab]
        lab_rows.insert(0, " 0123456789")
        for i in range(0, 10, 1):
            lab_rows[i + 1] = str(i) + lab_rows[i + 1]
        return "\n".join(lab_rows)

    def print_lab(self):
        print(self.get_map())
        print(20 * "-")

    def set_char_on_lab(self, char):
        self.lab[self.position.y][self.position.x] = char

    def count_x(self):
        return self.get_map().count("X")

    def move(self):
        if self.ahead() == "#":
            self.turn_right()
            # print("turn left")
        elif self.ahead() is None:
            # print("end of map")
            self.set_char_on_lab("X")
            final_map = self.get_map()
            # print(self.count_x())
            return False
        else:
            self.set_char_on_lab("X")
            self.position += self.direction
            self.set_char_on_lab(self.get_direction_char())
            log = (self.position, self.direction)
            if log in self.walk_log:
                self.log_movement()
                self.is_looping = True
                return False
        self.log_movement()
        return True


# part 1
print("part 1")
x = puzzle.splitlines()
print(len(x), len(x[0]))
guard = Guard(puzzle)
while guard.move():
    pass
print("result", guard.count_x())

# part 2

from multiprocessing import Pool

print("part 2")
positions = set(copy(position) for position, direction in guard.walk_log)


def looping_at_position(position):
    guard = Guard(puzzle=puzzle, extra_obstruction=position)
    while guard.move():
        pass
    return guard.is_looping


pool = Pool(12)
results = pool.map(looping_at_position, positions)
pool.close()
pool.join()
print(len(results))
print(results.count(True))
