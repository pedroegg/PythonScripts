from collections import deque
from typing import List, Deque, Tuple

def findCircleNum(isConnected: List[List[int]]) -> int:
	n = len(isConnected)
	visited = [False] * n
	provinces = 0

	def visit_all_connected_nodes(city: int) -> None:
		queue = deque([city])
		visited[city] = True

		while queue:
			node = queue.popleft()
			for related_city in range(n):
				if isConnected[node][related_city] and not visited[related_city]:
					visited[related_city] = True
					queue.append(related_city)

	for city in range(n):
		if not visited[city]:
			provinces += 1
			visit_all_connected_nodes(city)

	return provinces

#funciona mas com baixo desempenho
def numIslands(grid: List[List[str]]) -> int:
	if not grid:
		return 0

	m = len(grid)
	n = len(grid[0])

	visited = set()
	islands = 0

	def visit_island_nodes(point: tuple) -> None:
		queue = deque([point])

		while queue:
			point = queue.popleft()
			x, y = point[0], point[1]

			if point not in visited:
				visited.add(point)

				if grid[x][y] == '1':
					if x+1 < m:
						queue.append((x+1, y))

					if y+1 < n:
						queue.append((x, y+1))

					if x-1 >= 0:
						queue.append((x-1, y))

					if y-1 >= 0:
						queue.append((x, y-1))

	for x in range(m):
		for y in range(n):
			point = (x, y)

			if grid[x][y] == '1' and point not in visited:
				islands += 1
				visit_island_nodes(point)

	return islands

#versão otimizada, sem usar set "colorindo" a própria matriz e mais legível
def numIslandsV2(grid: List[List[str]]) -> int:
	if not grid:
		return 0

	m = len(grid)
	n = len(grid[0])
	islands = 0
	directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

	def visit_linked_islands(x: int, y: int) -> None:
		queue: Deque[Tuple[int, int]] = deque([(x, y)])

		while queue:
			x, y = queue.popleft()

			for dx, dy in directions:
				nx, ny = x + dx, y + dy

				valid_x = 0 <= nx < m
				valid_y = 0 <= ny < n

				if valid_x and valid_y and grid[nx][ny] == '1':
					grid[nx][ny] = '0'
					queue.append((nx, ny))

	for x in range(m):
		for y in range(n):
			if grid[x][y] != '1':
				continue

			islands += 1
			grid[x][y] = '0'

			visit_linked_islands(x, y)

	return islands

def floodFill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
	if not image:
		return [[]]

	color_to_overwrite = image[sr][sc]
	if color_to_overwrite == color:
		return image

	image[sr][sc] = color

	m = len(image)
	n = len(image[0])
	directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

	queue = deque([(sr, sc)])
	while queue:
		x, y = queue.popleft()

		for dx, dy in directions:
			nx, ny = x + dx, y + dy

			valid_x = 0 <= nx < m
			valid_y = 0 <= ny < n

			if valid_x and valid_y and image[nx][ny] == color_to_overwrite:
				image[nx][ny] = color
				queue.append((nx, ny))

	return image
