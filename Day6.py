# --- Day 6: Guard Gallivant ---
# The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.
#
# You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.
#
# Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?
#
# You start by making a map (your puzzle input) of the situation. For example:
#
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.
#
# Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:
#
# If there is something directly in front of you, turn right 90 degrees.
# Otherwise, take a step forward.
# Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):
#
# ....#.....
# ....^....#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...
# Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:
#
# ....#.....
# ........>#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...
# Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:
#
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#......v.
# ........#.
# #.........
# ......#...
# This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):
#
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#v..
# By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:
#
# ....#.....
# ....XXXXX#
# ....X...X.
# ..#.X...X.
# ..XXXXX#X.
# ..X.X.X.X.
# .#XXXXXXX.
# .XXXXXXX#.
# #XXXXXXX..
# ......#X..
# In this example, the guard will visit 41 distinct positions on your map.
#
# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

map_input = [
	"....#.....",
	".........#",
	"..........",
	"..#.......",
	".......#..",
	"..........",
	".#..^.....",
	"........#.",
	"#.........",
	"......#..."
]

def read_map(map_input):
	start_position = None
	guard_direction = None
	updated_map = []

	# Iterate through each row and character to find the guard and update the map
	for row_index, row in enumerate(map_input):
		new_row = ""
		for col_index, char in enumerate(row):
			if char in "^v<>":  # Identify the guard based on direction
				start_position = (row_index, col_index)
				guard_direction = char
				new_row += "."  # Replace guard symbol with a space in the initial map
			else:
				new_row += char

		updated_map.append(list(new_row))  # Convert rows to mutable lists for easy updates

	return start_position, guard_direction, updated_map

def process_guard_movement(map_input, guard_position, guard_direction):
	row, col = guard_position
	movement_string = check_guard_direction(row, col, guard_direction, map_input)

	# Check for an obstacle and count steps
	obstacle_index = movement_string.find('#')
	if obstacle_index != -1:
		obstacle_exists = True
		spaces_until_obstacle = obstacle_index  # Spaces until the next obstacle
		reached_edge = False  # Did not reach the edge, obstacle in the way
	else:
		obstacle_exists = False
		spaces_until_obstacle = len(movement_string)  # The entire path until the edge
		reached_edge = True  # Path leads to the edge of the map

	return obstacle_exists, spaces_until_obstacle, reached_edge

def check_guard_direction(row, col, guard_direction, map_input):
	# Determine the string to check (row or column) based on movement direction
	if guard_direction == '>':  # Moving right
		movement_string = "".join(map_input[row][col + 1:])  # Extract from (col+1) to the end of the row
	elif guard_direction == '<':  # Moving left
		movement_string = "".join(
			map_input[row][:col][::-1])  # Extract from start to (col) and reverse for left movement
	elif guard_direction == 'v':  # Moving down
		movement_string = "".join(map_input[i][col] for i in range(row + 1, len(map_input)))  # Extract column downward
	elif guard_direction == '^':  # Moving up
		movement_string = "".join(map_input[i][col] for i in range(row - 1, -1, -1))  # Extract column upward
	else:
		raise ValueError(f"Invalid guard direction: {guard_direction}")
	return movement_string

def update_guard_direction(direction):
	direction_mapping = {
		'>': 'v',  # Right to Down
		'v': '<',  # Down to Left
		'<': '^',  # Left to Up
		'^': '>'  # Up to Right
	}
	return direction_mapping[direction]

def update_map_with_guard_path(map_input, guard_position, spaces_to_move, guard_direction):
	row, col = guard_position

	for step in range(spaces_to_move):
		# Mark the current position as visited
		map_input[row][col] = "X"

		# Update the guard's position based on the direction
		if guard_direction == '>':  # Moving right
			col += 1
		elif guard_direction == '<':  # Moving left
			col -= 1
		elif guard_direction == 'v':  # Moving down
			row += 1
		elif guard_direction == '^':  # Moving up
			row -= 1

		# Stop marking if we reach the bounds of the map
		# Guard has exited
		if row < 0 or row >= len(map_input) or col < 0 or col >= len(map_input[0]):
			break

	# Ensure that the last valid position is marked before break
	if 0 <= row < len(map_input) and 0 <= col < len(map_input[0]):
		map_input[row][col] = "X"

	return row, col


def count_visited_spaces(map):
	visited_spaces = 0
	for row in map:
		visited_spaces += row.count("X")
	return visited_spaces

def main(map_input):
	start_position, guard_direction, updated_map = read_map(map_input)
	current_position = start_position

	step_number = 1

	while True:
		print(f"Step {step_number}:")
		print(f"  Guard is currently at position {current_position} facing {guard_direction}.")

		# Process guard's movement
		obstacle_exists, spaces_to_move, reached_edge = process_guard_movement(updated_map, current_position,
																			   guard_direction)

		if reached_edge:
			print(f"  Guard will move {spaces_to_move} spaces until the edge of the map and then exit.")
			current_position = update_map_with_guard_path(updated_map, current_position, spaces_to_move,
														  guard_direction)
			break

		print(f"  Guard will move {spaces_to_move} spaces before encountering an obstacle.") if obstacle_exists else \
			print(f"  Guard will move {spaces_to_move} spaces with no obstacles in the way.")

		current_position = update_map_with_guard_path(updated_map, current_position, spaces_to_move, guard_direction)

		if obstacle_exists:
			guard_direction = update_guard_direction(guard_direction)
			print(f"  Guard encounters an obstacle and turns to face {guard_direction}.")

		print("  Current map state:")
		for row in updated_map:
			print("".join(row))

		print("\n")
		step_number += 1

	# Print and count the final results
	print("Final map after guard path traversal:")
	for row in updated_map:
		print("".join(row))

	count = count_visited_spaces(updated_map)
	print(f"Total number of distinct positions visited by the guard: {count}")
	return count


print(f"Total visited spaces: {main(map_input)}")

with open('Day6_input.txt', 'r') as f:
	input = f.read()

print(f"Total visited spaces: {main(input.splitlines(keepends=False))}")