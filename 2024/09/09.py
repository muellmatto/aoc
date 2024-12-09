testcase = "2333133121414131402"

testcase_steps = """00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566.............."""

testcase_result = 1928

testcase_steps_part2 = """00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888.."""

testcase_result_part_2 = 2858


def build_blocks(puzzle):
    blocks = []
    file_id = -1
    for index, number in enumerate(puzzle.strip("\n")):
        if index % 2 == 0:  # number is length of a file
            file_id += 1
            for _ in range(int(number)):
                blocks.append(file_id)
        else:  # number is lenght of free space
            for _ in range(int(number)):
                blocks.append(".")
    return blocks, file_id


def swap_blocks(index_1, index_2, blocks):
    return swap_slices(index_1, index_2, length=1, blocks=blocks)


def swap_slices(index_1, index_2, length, blocks):
    blocks[index_1 : index_1 + length], blocks[index_2 : index_2 + length] = (
        blocks[index_2 : index_2 + length],
        blocks[index_1 : index_1 + length],
    )
    return blocks


def get_rightmost_file_index(blocks):
    # r-find first non ".":
    for index in range(len(blocks) - 1, -1, -1):
        if blocks[index] != ".":
            return index


def get_file_position(file_id, blocks, start_position=0):
    try:
        start_position = blocks.index(file_id, start_position)
    except ValueError:
        return False
    end_position = start_position
    size = len(blocks)
    while blocks[end_position] == file_id:
        end_position += 1
        if end_position >= size:
            break
    return start_position, end_position


def get_free_space_for_filesize(blocks, filesize):
    start_position = 0
    while True:
        free_space = get_file_position(".", blocks, start_position=start_position)
        if free_space:
            start, end = free_space
            if filesize <= end - start:
                return start
            else:
                start_position = end + 1
        else:
            return False


def defrag(blocks):
    # steps = "".join(map(str, blocks))
    while blocks.index(".") < len(blocks) - blocks.count("."):
        index_last_file = get_rightmost_file_index(blocks)
        index_first_free_space = blocks.index(".")
        blocks = swap_blocks(index_last_file, index_first_free_space, blocks)
        # steps += "\n" + "".join(map(str, blocks))
    # assert steps == testcase_steps
    return blocks


def calculate_checksum(blocks):
    checksum = 0
    for index, number in enumerate(blocks):
        if number != ".":
            checksum += index * int(number)

    return checksum


def defrag_part_2(blocks, max_file_id):
    # steps = "".join(map(str, blocks))
    for file_id in range(max_file_id, -1, -1):
        file_start, file_end = get_file_position(file_id, blocks)
        filesize = file_end - file_start
        free_space_start = get_free_space_for_filesize(blocks, filesize)
        if free_space_start:
            if free_space_start < file_start:
                blocks = swap_slices(file_start, free_space_start, filesize, blocks)
                # steps += "\n" + "".join(map(str, blocks))
    # assert steps == testcase_steps_part2
    return blocks


if __name__ == "__main__":
    print("testcase part 1")
    blocks, max_file_id = build_blocks(testcase)
    print(calculate_checksum(defrag(blocks)))

    print("testcase part 2")
    blocks, max_file_id = build_blocks(testcase)
    print(calculate_checksum(defrag_part_2(blocks, max_file_id)))

    with open("input", "r") as f:
        puzzle = f.read()

    print("part 1")
    blocks, max_file_id = build_blocks(puzzle)
    print(calculate_checksum(defrag(blocks)))

    print("part 2")
    blocks, max_file_id = build_blocks(puzzle)
    print(calculate_checksum(defrag_part_2(blocks, max_file_id)))
