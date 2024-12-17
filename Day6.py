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
		# print(f"Step {step_number}:")
		# print(f"  Guard is currently at position {current_position} facing {guard_direction}.")

		# Process guard's movement
		obstacle_exists, spaces_to_move, reached_edge = process_guard_movement(updated_map, current_position,
																			   guard_direction)

		if reached_edge:
			update_map_with_guard_path(updated_map, current_position, spaces_to_move,
														  guard_direction)
			break


		current_position = update_map_with_guard_path(updated_map, current_position, spaces_to_move, guard_direction)

		if obstacle_exists:
			guard_direction = update_guard_direction(guard_direction)

		# print("\n")
		step_number += 1

	# Print and count the final results
	# print("Final map after guard path traversal:")
	# for row in updated_map:
	# 	print("".join(row))

	count = count_visited_spaces(updated_map)
	# print(f"Total number of distinct positions visited by the guard: {count}")
	return count, updated_map




with open('Day6_input.txt', 'r') as f:
	input = f.read()

visisted_spaces, final_map = main(input.splitlines())

# --- Part Two ---
# While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.
#
# Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.
#
# Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.
#
# To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.
#
# In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.
#
# Option one, put a printing press next to the guard's starting position:
#
# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ....|..#|.
# ....|...|.
# .#.O^---+.
# ........#.
# #.........
# ......#...
# Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:
#
#
# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ......O.#.
# #.........
# ......#...
# Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:
#
# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----+O#.
# #+----+...
# ......#...
# Option four, put an alchemical retroencabulator near the bottom left corner:
#
# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ..|...|.#.
# #O+---+...
# ......#...
# Option five, put the alchemical retroencabulator a bit to the right instead:
#
# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ....|.|.#.
# #..O+-+...
# ......#...
# Option six, put a tank of sovereign glue right next to the tank of universal solvent:
#
# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----++#.
# #+----++..
# ......#O..
# It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.
#
# You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

def check_obstructions(map_input, guard_position, guard_direction):
	# Set to store visited states (position and direction)
	obstructions = set()

	# Current state of the guard
	current_position = guard_position
	current_direction = guard_direction

	while True:
		guard_state = (current_position[0], current_position[1], current_direction)

		# Check if this state has been visited before
		if guard_state in obstructions:
			print(f"Loop detected: guard is stuck at state {guard_state}.")
			return True  # Loop detected

		# Add the current state to obstructions
		obstructions.add(guard_state)

		# Process the guard's movement
		obstacle_exists, spaces_to_move, reached_edge = process_guard_movement(
			map_input, current_position, current_direction
		)

		# Update the map with the guard’s path
		current_position = update_map_with_guard_path(
			map_input, current_position, spaces_to_move, current_direction
		)

		# Check if the guard has exited the map
		if reached_edge:
			print(f"Guard has exited the map at {current_position}. No loop.")
			return False  # No loop

		# Update direction if an obstacle is encountered
		if obstacle_exists:
			current_direction = update_guard_direction(current_direction)

def get_visited_locations(map_input):
	visited_locations = set()  # Use a set to store unique visited positions

	# Iterate through rows and columns of the map
	for row_idx, row in enumerate(map_input):
		for col_idx, cell in enumerate(row):
			if cell == "X":  # Check if the cell is visited ("X")
				visited_locations.add((row_idx, col_idx))  # Add (row_idx, col_idx) to the set

	# Debug: Print visited locations
	if len(visited_locations) == 0:
		print("No visited locations ('X') found in the map.")
	else:
		print(f"Visited locations: {visited_locations}")

	return visited_locations


def check_all_obstructions(map_input, guard_position, guard_direction):
	# Step 1: Track all visited locations
	visited_locations = get_visited_locations(map_input)
	print(f"Total number of visited locations: {len(visited_locations)}")

	looping_positions = []  # To store locations that cause a loop

	for position in visited_locations:
		# Step 2: Modify the map to place an obstacle at the position
		row, col = position
		original_char = map_input[row][col]  # Save the original value
		map_input[row][col] = '#'  # Mark as an obstacle

		# Step 3: Check if the map now causes a loop
		if check_obstructions(map_input, guard_position, guard_direction):
			looping_positions.append(position)  # Record the position if it causes a loop

		# Step 4: Restore the map
		map_input[row][col] = original_char  # Reset the location

	# Step 5: Return the looping positions
	return looping_positions

def part_2():
	start_position, guard_direction, updated_map = read_map(input.splitlines())
	# print(updated_map)
	_, final_map = main(input.splitlines())
	# print(final_map)
	looping_positions = check_all_obstructions(final_map, start_position, guard_direction)
	return looping_positions

print(len(part_2()))
