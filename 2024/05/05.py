testcase = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def get_updates_and_rules(puzzle):
    rules_raw, updates_raw = puzzle.split("\n\n")
    rules = rules_raw.splitlines()
    updates = [line.split(",") for line in updates_raw.splitlines()]
    return updates, rules


def update_complies_with_rule(update, rule):
    a, b = rule.split("|")
    if a in update and b in update:
        if update.index(a) < update.index(b):
            return True
        else:
            return False
    return True


def update_complies_all_rules(update, rules):
    for rule in rules:
        if not update_complies_with_rule(update, rule):
            return False
    return True


def get_correct_updates(updates, rules):
    correct_updates = [
        update for update in updates if update_complies_all_rules(update, rules)
    ]
    return correct_updates


def get_middle_page(update):
    return int(update[len(update) // 2])


def sum_middle_pages(updates):
    middle_pages = [get_middle_page(update) for update in updates]
    return sum(middle_pages)


def solve_part_1(puzzle):
    return sum_middle_pages(get_correct_updates(*get_updates_and_rules(puzzle)))


def get_incorrect_updates(updates, rules):
    incorrect_updates = [
        update for update in updates if not update_complies_all_rules(update, rules)
    ]
    return incorrect_updates


def apply_rule_on_update(update, rule):
    a, b = rule.split("|")
    if a in update and b in update:
        if not update_complies_with_rule(update, rule):
            page_to_move = update.pop(update.index(b))
            update.insert(update.index(a) + 1, page_to_move)
    return update


def apply_all_rules_on_update(update, rules):
    for rule in rules:
        update = apply_rule_on_update(update, rule)
    if update_complies_all_rules(update, rules):
        return update
    else:
        return apply_all_rules_on_update(update, rules)


def solve_part_2(puzzle):
    updates, rules = get_updates_and_rules(puzzle)
    incorrect_updates = get_incorrect_updates(updates, rules)
    fixed_updates = [
        apply_all_rules_on_update(update, rules) for update in incorrect_updates
    ]
    return sum_middle_pages(fixed_updates)


with open("input", "r") as f:
    puzzle = f.read()

print("Part 1")
print(solve_part_1(puzzle))

print("part 2")
print(solve_part_2(puzzle))
