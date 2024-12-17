# --- Day 4: Ceres Search ---
# "Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!
#
# As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.
#
# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:
#
#
# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
# The actual word search will be full of letters instead. For example:
#
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:
#
# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# Take a look at the little Elf's word search. How many times does XMAS appear?

input = ('Day4_input.txt')

with open(input, 'r') as f:
	data = f.read()


def get_neighbours(matrix, row, col):
	"""Fetches all valid neighbors of a given element in the matrix."""
	rows, cols = len(matrix), len(matrix[0])
	directions = [
		(-1, -1), (-1, 0), (-1, 1),  # Top-left, top, top-right
		(0, -1), (0, 1),  # Left,      right
		(1, -1), (1, 0), (1, 1)  # Bottom-left, bottom, bottom-right
	]
	neighbours = []

	for dr, dc in directions:
		r, c = row + dr, col + dc
		if 0 <= r < rows and 0 <= c < cols:  # Ensure neighbors are within bounds
			neighbours.append(matrix[r][c])

	return neighbours


# Input matrix
input_matrix = [
	['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'],
	['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'],
	['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'],
	['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'],
	['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'],
	['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'],
	['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'],
	['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'],
	['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'],
	['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']
]


def extract_diagonals(matrix):
	"""
    Extracts all diagonals (both directions) from a 2D matrix and concatenates their characters into strings.

    :param matrix: List of Lists representing the 2D matrix
    :return: A list of strings, each representing a diagonal
    """
	rows = len(matrix)
	cols = len(matrix[0])

	diagonals = []

	# Collect all top-left to bottom-right (\) diagonals
	for d in range(rows + cols - 1):
		diagonal = []
		for row in range(rows):
			col = d - row
			if 0 <= col < cols:
				diagonal.append(matrix[row][col])
		if diagonal:
			diagonals.append("".join(diagonal))

	# Collect all top-right to bottom-left (/) diagonals
	for d in range(-cols + 1, rows):
		diagonal = []
		for row in range(rows):
			col = row - d
			if 0 <= col < cols:
				diagonal.append(matrix[row][col])
		if diagonal:
			diagonals.append("".join(diagonal))

	return diagonals


# Example usage:
input_matrix = [
	['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'],
	['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'],
	['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'],
	['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'],
	['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'],
	['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'],
	['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'],
	['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'],
	['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'],
	['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']
]

diagonals = extract_diagonals(input_matrix)


def check_string_in_rows(matrix, search_string):
	string_count = 0
	for row in matrix:
		concatenated_row = "".join(row)
		string_count += concatenated_row.count(search_string)
		# reverse the string and count again for backwards direction
		concatenated_row_reversed = "".join(reversed(row))
		string_count += concatenated_row_reversed.count(search_string)

	# Transpose the matrix - rows to columns and columns to row
	transposed_matrix = list(map(list, zip(*matrix)))
	for row in transposed_matrix:
		concatenated_row = "".join(row)
		string_count += concatenated_row.count(search_string)
		concatenated_row_reversed = "".join(reversed(row))
		string_count += concatenated_row_reversed.count(search_string)

	# Now convert the matrix into a series of strings along diagonals and check the forward and backward strings
	diagonals = extract_diagonals(matrix)
	for diagonal in diagonals:
		string_count += diagonal.count(search_string)
		string_count += diagonal[::-1].count(search_string)

	return string_count

result = check_string_in_rows(input_matrix, "XMAS")
print(result)

file_path = 'Day4_input.txt'

with open(file_path, 'r') as f:
	matrix = [list(line.strip()) for line in f.readlines()]

answer = check_string_in_rows(matrix, "XMAS")
print(answer)

# --- Part Two ---
# The Elf looks quizzically at you. Did you misunderstand the assignment?
#
# Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:
#
# M.S
# .A.
# M.S
# Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.
#
# Here's the same example from before, but this time all of the X-MASes have been kept instead:
#
# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........
# In this example, an X-MAS appears 9 times.
#
# Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

test_matrix = [
	['.', 'M', '.', 'S', '.', '.', '.', '.', '.', '.'],
	['.', '.', 'A', '.', '.', 'M', 'S', 'M', 'S', '.'],
	['.', 'M', '.', 'S', '.', 'M', 'A', 'A', '.', '.'],
	['.', '.', 'A', '.', 'A', 'S', 'M', 'S', 'M', '.'],
	['.', 'M', '.', 'S', '.', 'M', '.', '.', '.', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
	['S', '.', 'S', '.', 'S', '.', 'S', '.', 'S', '.'],
	['.', 'A', '.', 'A', '.', 'A', '.', 'A', '.', '.'],
	['M', '.', 'M', '.', 'M', '.', 'M', '.', 'M', '.'],
	['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
]



def count_a_with_diagonal_neighbours(matrix):
	rows = len(matrix)
	cols = len(matrix[0]) if rows > 0 else 0
	count = 0

	# No need to check very edge of array, since that won't be a valid location for X-MAS
	for i in range(rows):
		for j in range(cols):
			if matrix[i][j] == 'A':
				# List all diagonal neighbors
				diagonal_neighbors = [
					(i - 1, j - 1),  # top-left
					(i - 1, j + 1),  # top-right
					(i + 1, j + 1),  # bottom-right
					(i + 1, j - 1)  # bottom-left
				]

				neighbor_chars = []
				for x, y in diagonal_neighbors:
					if 0 <= x < rows and 0 <= y < cols:  # Ensure within bounds
						neighbor_chars.append(matrix[x][y])

				# There's 4 allowed orders for the neighbours ot make an X-MAS
				allowed_sequences = ['MMSS', 'SMMS', 'SSMM', 'MSSM']
				if "".join(neighbor_chars) in allowed_sequences:
					count += 1


	return count

result = count_a_with_diagonal_neighbours(test_matrix)
print(result)

answer2 = count_a_with_diagonal_neighbours(matrix)
print(answer2)