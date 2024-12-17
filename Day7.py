# --- Day 7: Bridge Repair ---
# The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?
#
# When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.
#
# You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).
#
# For example:
#
# 190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.
#
# Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).
#
# Only three of the above equations can be made true by inserting operators:
#
# 190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
# 3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
# 292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
# The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.
#
# Determine which equations could possibly be true. What is their total calibration result?

from itertools import product

test_array = [
	"190: 10 19",
	"3267: 81 40 27",
	"83: 17 5",
	"156: 15 6",
	"7290: 6 8 6 15",
	"161011: 16 10 13",
	"192: 17 8 14",
	"21037: 9 7 18 13",
	"292: 11 6 16 20"
]

def main(data, concat=False):
	valid_test_values_sum = 0  # To keep track of the sum of valid test values

	for line in data:
		# Split the test data into test_value and operators
		test_value, operators = split_test_data(line)
		# print(test_value, operators)

		# Generate all possible test equations from the operators
		test_equations = generate_test_equations(operators, concat=concat)

		# Check if any equation evaluates to the test_value
		test_value_valid = False
		for equation in test_equations:
			result = evaluate_test_equation_ltr(equation)
			# print(equation, result)
			if result == test_value:
				test_value_valid = True
				break

		# If valid, add the test_value to the sum
		if test_value_valid:
			valid_test_values_sum += test_value

	return valid_test_values_sum

# Function to split the string into test_value and operators
def split_test_data(data):
	test_value, operators = data.split(':')  # Split on ':'
	test_value = int(test_value.strip())  # Convert test_value to an integer
	operators = list(map(int, operators.strip().split())) # Extract integers from operators
	return test_value, operators


def evaluate_test_equation_ltr(equation):
	# Custom evaluation function, breaks normal math rules
	# Split the equation into tokens (numbers and operators)
	tokens = equation.split()

	# Initialize the result with the first number
	result = int(tokens[0])

	# Apply each operator and number sequentially, left-to-right
	for i in range(1, len(tokens), 2):
		operator = tokens[i]
		number = int(tokens[i + 1])

		if operator == "+":
			result += number
		elif operator == "*":
			result *= number
		elif operator == "||":
			# Concatenate the digits using string conversion
			result = int(str(result) + str(number))
		else:
			raise ValueError(f"Invalid operator: {operator}")

	return result

def generate_test_equations(operators, concat=False):
	"""
    Generates all possible equations by placing +, *, and || between operators.
    """
	if len(operators) == 1:
		return [str(operators[0])]  # Base case: only one number

	# Generate all possible sequences of +, *, and || for (n-1) positions
	if concat is False:
		operator_symbols = ['+', '*']
	else:
		operator_symbols = ['+', '*', '||']

	symbol_combinations = list(product(operator_symbols, repeat=len(operators) - 1))

	equations = []
	for symbols in symbol_combinations:
		equation = str(operators[0])  # Start with the first number
		for i, symbol in enumerate(symbols):
			equation += f" {symbol} {operators[i + 1]}"  # Add operator and next number
		equations.append(equation)

	return equations

with open("Day7_input.txt", "r") as file:
	data = file.read().splitlines()

print(main(data))

print(main(data, concat=True))


# --- Part Two ---
# The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.
#
# The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.
#
# Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:
#
# 156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
# 7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
# 192: 17 8 14 can be made true using 17 || 8 + 14.
# Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.
#
# Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?

