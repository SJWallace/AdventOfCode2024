# @formatter:on
# --- Day 9: Disk Fragmenter ---
# Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each
# somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving
# directly into walls.
#
# While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling
# with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program
# isn't working; you offer to help.
#
# He shows you the disk map (your puzzle input) he's already generated. For example:
#
# 2333133121414131402
# The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate
# between indicating the length of a file and the length of free space.
#
# So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file,
# four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files
# in a row (with no free space between them).
#
# Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged,
# starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID
# 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free
# space, the disk map 12345 represents these individual blocks:
#
# 0..111....22222
# The first example above, 2333133121414131402, represents these individual blocks:
#
# 00...111...2...333.44.5555.6666.777.888899
# The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block
# (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:
#
# 0..111....22222
# 02.111....2222.
# 022111....222..
# 0221112...22...
# 02211122..2....
# 022111222......
# The first example requires a few more steps:
#
# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............
# The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum,
# add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost
# block is in position 0. If a block contains free space, skip it instead.
#
# Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0,
# 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.
#
# Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be
# careful copy/pasting the input for this puzzle; it is a single, very long line.)

from collections import deque

class DiskMap():
	def __init__(self, disk_map):
		self.disk_map = disk_map
		self.blocks = deque
		self.parse_disk_map()

	def parse_disk_map(self):
		"""
		Parses the input disk map string into blocks and updates the representations. The parsed list contains file IDs
		for file blocks and `.` for free space.
		"""
		parsed_map = []
		file_id = 0

		for idx, length in enumerate(map(int, self.disk_map)):
			if idx % 2 != 0:  # Even index (file length or free space based on the problem description)
				parsed_map.extend(["."] * length)  # Add free space as `.`
			else:  # Odd index (file length)
				parsed_map.extend([str(file_id)] * length)  # Add file blocks with incremental file ID
				file_id += 1

		self.blocks = parsed_map

	def defrag_disk(self):
		"""
		Defragments the disk by moving file blocks to the left and compacting all the free space dots ('.') to the right.
		"""
		leftmost_free_index = 0

		while True:
			# Find the rightmost file block
			rightmost_index = len(self.blocks) - 1
			while rightmost_index >= 0 and self.blocks[rightmost_index] == '.':
				rightmost_index -= 1

			# If no file blocks remain (all spaces are '.')
			if rightmost_index < 0:
				break

			# Find the first free space ('.') starting from leftmost_free_index
			while leftmost_free_index < rightmost_index and self.blocks[leftmost_free_index] != '.':
				leftmost_free_index += 1

			# If the leftmost free index is already past the rightmost file block, we are done
			if leftmost_free_index >= rightmost_index:
				break

			# Move the file block to the leftmost free space
			self.blocks[leftmost_free_index] = self.blocks[rightmost_index]
			self.blocks[rightmost_index] = '.'

			# Update leftmost_free_index to continue the iteration
			leftmost_free_index += 1

	def calculate_checksum(self):
		"""
		Calculates the checksum of the disk. For each file block (non-dot value),
		its index is multiplied by its value and added to the checksum.
		Stops summing as soon as a free space ('.') is encountered.
		"""
		checksum = 0

		for index, value in enumerate(self.blocks):
			if value == '.':  # Stop calculation if a free space is encountered
				break
			checksum += index * int(value)  # Convert value to int and add to checksum

		return checksum



	def print_disk(self):
		"""
		Prints the current state of the disk's blocks representation.
		"""
		print("".join(self.blocks))


test_diskmap = DiskMap("2333133121414131402")
test_diskmap.print_disk()
test_diskmap.defrag_disk()
test_diskmap.print_disk()
print(test_diskmap.calculate_checksum())

#
day9_diskmap = DiskMap(open('Day9_input.txt').read())
day9_diskmap.defrag_disk()
day9_diskmap.print_disk()
print(day9_diskmap.calculate_checksum())