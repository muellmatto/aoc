with open("input.txt", "r") as f:
    reports = f.read().splitlines()


def is_decreasing(levels):
    for i in range(len(levels) - 1):
        x, y = levels[i : i + 2]
        x, y = int(x), int(y)
        if (x - y > 3) or (x - y < 1):
            return False
    return True


def is_increasing(levels):
    for i in range(len(levels) - 1):
        x, y = levels[i : i + 2]
        x, y = int(x), int(y)
        if (y - x > 3) or (y - x < 1):
            return False
    return True


reports_safe = []
reports_unsafe = []

for report in reports:
    levels = report.split(" ")
    if is_decreasing(levels):
        reports_safe.append(report)
    elif is_increasing(levels):
        reports_safe.append(report)
    else:
        reports_unsafe.append(report)

print("part 1")
print("all:", len(reports))
print("unsafe:", len(reports_unsafe))
print("safe:", len(reports_safe))

print("part 2")
# Problem Dampener
reports_fixed = []
reports_still_unsafe = []
for report in reports_unsafe:
    problem_damper_success = False
    levels = report.split(" ")

    for i in range(len(levels)):
        sub_levels = levels[0:i] + levels[i + 1 :]
        if is_decreasing(sub_levels):
            print(levels)
            print(sub_levels)
            problem_damper_success = True
            reports_fixed.append(report)
            break
        elif is_increasing(sub_levels):
            problem_damper_success = True
            reports_fixed.append(report)
            break
    if not problem_damper_success:
        reports_still_unsafe.append(report)

print("fixed:", len(reports_fixed))
print("still unsafe:", len(reports_still_unsafe))
print("new_safe:", len(reports_fixed) + len(reports_safe))
