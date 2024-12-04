import re

testcase = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
# result: 161 (2*4 + 5*5 + 11*8 + 8*5)

# pattern = r"mul\(\d{1,3},\d{1,3}\)"
# x = re.findall(pattern, testcase)
# print(x)


def mull_it(data):
    pattern_groups = r"mul\((\d{1,3}),(\d{1,3})\)"
    pairs = re.findall(pattern_groups, data)
    products = [int(pair[0]) * int(pair[1]) for pair in pairs]
    return sum(products)


print("testcase:", mull_it(testcase))

with open("input.txt", "r") as f:
    data = f.read()

print("pasrt 1:", mull_it(data))

do_s_split = data.split("do()")
do_s = []
for do in do_s_split:
    donts = do.split("don't()")
    do_s.append(donts[0])

print("part 2", mull_it("".join(do_s)))
