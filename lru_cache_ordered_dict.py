from collections import OrderedDict

class LRUCache:
	def __init__(self, capacity: int):
		self.data = OrderedDict()
		self.capacity = capacity

	def get(self, key: int) -> int:
		if key not in self.data:
			return -1

		self.data.move_to_end(key, last=True)
		return self.data[key]

	def put(self, key: int, value: int) -> None:
		if key not in self.data and len(self.data) == self.capacity:
			self.data.popitem(last=False)

		if key in self.data:
			self.data.move_to_end(key, last=True)

		self.data[key] = value
