# --- Day 5: Print Queue ---
# Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.
#
# The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.
#
# The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.
#
# Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.
#
# The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.
#
# For example:
#
# 47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13
#
# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)
#
# The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.
#
# To get the printers going as soon as possible, start by identifying which updates are already in the right order.
#
# In the above example, the first update (75,47,61,53,29) is in the right order:
#
# 75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
# 47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
# 61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
# 53 is correctly fourth because it is before page number 29 (53|29).
# 29 is the only page left and so is correctly last.
# Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.
#
# The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.
#
# The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.
#
# The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.
#
# The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.
#
# For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:
#
# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.
#
# Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.
#
# Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?

test_input = """47|53
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

def parse_input(input: str):
	input_rules = []
	input_updates = []
	for line in input.splitlines():
		if not line.strip():
			continue
		if "|" in line:
			input_rules.append(line)
		else:
			input_updates.append(line)
	return input_rules, input_updates

def parse_rules(rules: list):
	split_rules = [tuple(map(int, rule.split("|"))) for rule in rules]
	return split_rules

def calculate_middle_sum(updates):
	middle_sum = 0
	for update in updates:
		middle_index = len(update) // 2
		middle_sum += update[middle_index]
	return middle_sum

def parse_updates(updates, rules):
	valid_updates = []

	for update in updates:
		update_pages = list(map(int, update.split(",")))
		is_valid = True
		for rule in rules:
			first_page, second_page = rule
			if first_page in update_pages and second_page in update_pages:
				if update_pages.index(first_page) < update_pages.index(second_page):
					continue
				else:
					is_valid = False
					break
			else:
				continue
		if is_valid:
			valid_updates.append(update_pages)
	middle_sum = calculate_middle_sum(valid_updates)

	return middle_sum

def page_sorter(input):
	rules, updates = parse_input(input)
	parsed_rules = parse_rules(rules)
	middle_sum = parse_updates(updates, parsed_rules)
	return middle_sum

with open("Day5_input.txt") as file:
	data = file.read()

result = page_sorter(data)
print(result)

# --- Part Two ---
# While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.
#
# For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:
#
# 75,97,47,61,53 becomes 97,75,47,61,53.
# 61,13,29 becomes 61,29,13.
# 97,13,75,29,47 becomes 97,75,47,29,13.
# After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.
#
# Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

from collections import defaultdict, deque


def topological_sort(update_pages, rules):
	pages = set(update_pages)
	graph = defaultdict(list)
	in_degree = defaultdict(int)

	# Build the graph and in-degree count based on the rules
	for first_page, second_page in rules:
		if first_page in pages and second_page in pages:
			graph[first_page].append(second_page)
			in_degree[second_page] += 1
			if first_page not in in_degree:
				in_degree[first_page] = 0

	queue = deque([page for page in pages if in_degree[page] == 0])
	sorted_pages = []

	while queue:
		current_page = queue.popleft()
		sorted_pages.append(current_page)
		for neighbor in graph[current_page]:
			in_degree[neighbor] -= 1
			if in_degree[neighbor] == 0:
				queue.append(neighbor)

	# If not all pages are sorted, there is a cycle
	if len(sorted_pages) != len(pages):
		raise ValueError("Cycle detected in the pages.")

	return sorted_pages

def identify_invalid_updates(updates, rules):
	valid_updates = []
	invalid_updates = []

	for update in updates:
		update_pages = list(map(int, update.split(",")))
		is_valid = True
		for rule in rules:
			first_page, second_page = rule
			if first_page in update_pages and second_page in update_pages:
				if update_pages.index(first_page) < update_pages.index(second_page):
					continue
				else:
					is_valid = False
					break

		if is_valid:
			valid_updates.append(update_pages)
		else:
			invalid_updates.append(update_pages)

	return valid_updates, invalid_updates


def reorder_updates(updates, rules):
	reordered_updates = []
	for update in updates:
		try:
			reordered = topological_sort(update, rules)
			reordered_updates.append(reordered)
		except ValueError as e:
			print(f"Skipping update {update}: {e}")
			continue
	return reordered_updates


def main(input):
	rules, updates = parse_input(input)
	parsed_rules = parse_rules(rules)
	valid_updates, invalid_updates = identify_invalid_updates(updates, parsed_rules)
	reordered_updates = reorder_updates(invalid_updates, parsed_rules)
	middle_sum = calculate_middle_sum(reordered_updates)
	return middle_sum


print(main(test_input))

with open("Day5_input.txt") as file:
	data = file.read()

print(main(data))