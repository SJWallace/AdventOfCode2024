# --- Day 8: Resonant Collinearity ---
# You find yourselves on the roof of a top-secret Easter Bunny installation.
#
# While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise,
# it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate
# as a Christmas gift! Unthinkable!
#
# Scanning across the city, you find that there are actually many such antennas.
# Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit.
# You create a map (your puzzle input) of these antennas. For example:
#
# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............
# The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. I
# n particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency -
# but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency,
# there are two antinodes, one on either side of them.
#
# So, for these two antennas with frequency a, they create the two antinodes marked with #:
#
# ..........
# ...#......
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ......#...
# ..........
# ..........
# Adding a third antenna with the same frequency creates several more antinodes.
# It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:
#
# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......#...
# ..........
# ..........
# Antennas with different frequencies don't create antinodes;
# A and a count as different frequencies. However, antinodes can occur at locations that contain antennas.
# In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:
#
# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......A...
# ..........
# ..........
# The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:
#
# ......#....#
# ...#....0...
# ....#0....#.
# ..#....0....
# ....0....#..
# .#....A.....
# ...#........
# #......#....
# ........A...
# .........A..
# ..........#.
# ..........#.
# Because the topmost A-frequency antenna overlaps with a 0-frequency antinode,
# there are 14 total unique locations that contain an antinode within the bounds of the map.
#
# Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

from itertools import combinations

test_input = [
	"............",
	"........0...",
	".....0......",
	".......0....",
	"....0.......",
	"......A.....",
	"............",
	"............",
	"........A...",
	".........A..",
	"............",
	"............"
]


class AsciiMap:
	def __init__(self, ascii_map_string):
		self.start_map = self.ascii_map_parser(ascii_map_string)
		self.height = len(self.start_map)
		self.width = len(self.start_map[0]) if self.height > 0 else 0
		self.antennas = {}
		self.antinode_map = self.start_map.copy()

	def ascii_map_parser(self, map_string):
		"""
		Parse a list of strings into a validated ASCII map.

		:param map_strings: List of strings, where each string represents a row of the ASCII map.
		:return: A list of lists representing the ASCII map (each inner list is a row of characters).
		:raises ValueError: If the input is invalid (e.g., inconsistent row lengths).
		"""
		if not map_string or not all(isinstance(row, str) for row in map_string):
			raise ValueError("Input must be a non-empty list of strings.")

		# Ensure all rows have the same width for a rectangular ASCII map
		row_length = len(map_string[0])
		if any(len(row) != row_length for row in map_string):
			raise ValueError("All rows in the ASCII map must have the same length.")

		# Convert strings into a 2D list of characters
		return [list(row) for row in map_string]

	def get_char(self, x, y):
		if y < 0 or y >= self.height or x < 0 or x >= self.width:
			raise IndexError("Position out of map bounds!")
		return self.start_map[y][x]

	def set_char(self, x, y, char, map=None):
		if map is None:  # Default to self.antinode_map if no map is provided
			map = self.antinode_map
		if y < 0 or y >= self.height or x < 0 or x >= self.width:
			raise IndexError("Position out of map bounds!")
		map[y][x] = char

	def find_antennas(self):
		antenna_dict = {}
		for y, row in enumerate(self.start_map):
			for x, char in enumerate(row):
				if char != '.':  # If the character is not a dot
					if char not in antenna_dict:
						antenna_dict[char] = []
					antenna_dict[char].append((x, y))
		self.antennas = antenna_dict

	def list_antennas(self):
		print(self.antennas)

	def locate_antinode(self):
		antinodes = set()

		for key, locations in self.antennas.items():
			# Iterate through all unique pairs of antennas
			for (x1, y1), (x2, y2) in combinations(locations, 2):
				# Calculate directional differences and distances
				dx = x2 - x1
				dy = y2 - y1

				# Calculate two potential antinodes by extending the distance outward
				antinode1 = (x1 - dx, y1 - dy)
				antinode2 = (x2 + dx, y2 + dy)
				print(antinode1, antinode2)

				# Add valid antinodes within bounds
				if self._is_within_bounds(antinode1):
					antinodes.add(antinode1)
				if self._is_within_bounds(antinode2):
					antinodes.add(antinode2)

		self.antinodes = antinodes

	def locate_antinode_lines(self):
		antinodes = set()

		for key, locations in self.antennas.items():
			# Iterate through all unique pairs of antennas
			for (x1, y1), (x2, y2) in combinations(locations, 2):
				# Calculate directional differences and distances
				dx = x2 - x1
				dy = y2 - y1

				i = 0
				while True:
					# Compute antinodes for the current scale factor i
					antinode1 = (x1 - i * dx, y1 - i * dy)  # Extend backward from first antenna
					antinode2 = (x2 + i * dx, y2 + i * dy)  # Extend forward from second antenna

					valid1 = self._is_within_bounds(antinode1)  # Check bounds for antinode1
					valid2 = self._is_within_bounds(antinode2)  # Check bounds for antinode2

					# Add valid antinodes to the set
					if valid1:
						antinodes.add(antinode1)
					if valid2:
						antinodes.add(antinode2)

					# Stop the loop if both antinodes are out of bounds
					if not valid1 and not valid2:
						break

					# Increment i to extend further
					i += 1

		self.antinodes = antinodes

	def mark_antinodes(self):
		for antinode in self.antinodes:
			x, y = antinode
			self.set_char(x, y, '#')

	def _is_within_bounds(self, antinode):
		x, y = antinode
		return 0 <= x < self.width and 0 <= y < self.height

	def antinode_count(self):
		print(f" Antinodes: {len(self.antinodes)}")

	def print_antinode_map(self):
		for row in self.antinode_map:
			print(row)

	def print_start_map(self):
		for row in self.start_map:
			print(row)



testMap = AsciiMap(test_input)
testMap.print_start_map()
testMap.find_antennas()
testMap.locate_antinode()
testMap.mark_antinodes()
testMap.print_antinode_map()
testMap.antinode_count()

day8map = AsciiMap(open('Day8_input.txt').read().splitlines())
day8map.print_start_map()
day8map.find_antennas()
day8map.locate_antinode()
day8map.mark_antinodes()
day8map.print_antinode_map()
day8map.antinode_count()

testMap.locate_antinode_lines()
testMap.mark_antinodes()
testMap.print_antinode_map()
testMap.antinode_count()

day8map.locate_antinode_lines()
day8map.mark_antinodes()
day8map.print_antinode_map()
day8map.antinode_count()

# --- Part Two ---
# Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.
#
# Whoops!
#
# After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas
# of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna
# (unless that antenna is the only one of its frequency).
#
# So, these three T-frequency antennas now create many antinodes:
#
# T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........
# In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes!
# This brings the total number of antinodes in the above example to 9.
#
# The original example now has 34 antinodes, including the antinodes that appear on every antenna:
#
# ##....#....#
# .#.#....0...
# ..#.#0....#.
# ..##...0....
# ....0....#..
# .#...#A....#
# ...#..#.....
# #....#.#....
# ..#.....A...
# ....#....A..
# .#........#.
# ...#......##
# Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?