# Python program to get least cost path in a grid from
# top-left to bottom-right
from functools import cmp_to_key
from collections import defaultdict

def mycmp(a,b):
	# if a.moves_left < b.moves_left:
	# 	return (a.moves_left-b.moves_left)	
	if (a.distance == b.distance):
		if (a.x != b.x):
			return (a.x - b.x)
		else:
			return (a.y - b.y)
	return (a.distance - b.distance)

# structure for information of each cell
class cell:

	def __init__(self,x, y, distance, dir, moves_in_dir):
		self.x = x
		self.y = y
		self.distance = distance
		self.dir = dir
		self.moves_in_dir = moves_in_dir

import math

# Method returns minimum cost to reach bottom
# right from top left
def shortest(grid, row, col):
	dis = [[math.inf for i in range(col)]for j in range(row)]
	assert len(dis) == row
	assert len(dis[0]) == col

	# direction arrays for simplification of getting
	# neighbour
	dx = [-1, 0, 1, 0]
	dy = [0, 1, 0, -1]

	st = []

	# insert (0, 0) cell with 0 distance
	st.append(cell(0, 0, 0, (0,1), 0))
	st.append(cell(0, 0, 0, (1,0), 0))

	# We don't pay the cost of the starting square.
	dis[0][0] = 0#grid[0][0]

	prev = defaultdict(lambda: None)
	# loop for standard dijkstra's algorithm
	while st:

		# get the cell with minimum distance and delete
		# it from the set
		k = st[0]
		st = st[1:]
		
		# looping through all neighbours
		for i in range(4):

			x = k.x + dx[i]
			y = k.y + dy[i]

			_dir = (dx[i], dy[i])
			# don't turn around
			if _dir == (-k.dir[0], -k.dir[1]):
				continue
	
			# if not inside boundary, ignore them
			if x < 0 or y < 0 or x >= col or y >= row:
				continue

			moves_in_dir = k.moves_in_dir
			if _dir == k.dir:
				moves_in_dir += 1
				if moves_in_dir > 3:
					continue
			else:
				moves_in_dir = 1
			# 	# we had to change dir, and we moved 1
			# 	moves_left = 3

			# If distance from current cell is smaller, then
			# update distance of neighbour cell
			if (dis[y][x] > dis[k.y][k.x] + grid[y][x]) and moves_in_dir <= 3:
				# update the distance and insert new updated
				# cell in set
				dis[y][x] = dis[k.y][k.x] + grid[y][x]
				prev[(k.x,k.y)] = (x,y)
				st.append(cell(x, y, dis[y][x], _dir, moves_in_dir))

		st.sort(key=cmp_to_key(mycmp))

	# uncomment below code to print distance
	# of each cell from (0, 0)

	# for i in range(row):
	#	 for j in range(col):
	#		 print(dis[i][j] ,end= " ")
	#	 print()

	# dis[row - 1][col - 1] will represent final
	# distance of bottom right cell from top left cell
	#assert grid[0][0] == dis[0][0]

	# path = [(col-1,row-1)]
	# current = path[0]
	# while prev[current]:
	# 	path.append(prev[current])
	# 	current = prev[current]

	return dis[row - 1][col - 1]#, path