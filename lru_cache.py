from typing import Dict, Union

class Node:
	def __init__(self, key: int, value: int):
		self.previous: Union[Node, None] = None
		self.next: Union[Node, None] = None
		self.key = key
		self.value = value

class Queue:
	def __init__(self):
		self.head: Union[Node, None] = None
		self.tail: Union[Node, None] = None

	def add(self, key: int, value: int) -> Node:
		node = Node(key, value)

		if self.head is None:
			self.head = node
			self.tail = self.head

			return node

		node.previous = self.tail
		self.tail.next = node
		self.tail = self.tail.next

		return node

	def remove(self, node: Node) -> None:
		if not node:
			return

		if self.head == node:
			self.head = self.head.next
			if self.head:
				self.head.previous = None

			return

		if self.tail == node:
			self.tail = self.tail.previous
			self.tail.next = None

			return

		node.previous.next = node.next
		node.next.previous = node.previous
		node = None

class LRUCache:
	def __init__(self, capacity: int):
		self.data: Dict[int, Node] = {}
		self.capacity = capacity
		self.queue = Queue()

	def get(self, key: int) -> int:
		if key not in self.data:
			return -1

		value = self.data[key].value
		self.queue.remove(self.data[key])
		self.data[key] = self.queue.add(key, value)

		return value

	def put(self, key: int, value: int) -> None:
		if key not in self.data and len(self.data) == self.capacity:
			removed_key = self.queue.head.key
			self.queue.remove(self.queue.head)
			del self.data[removed_key]

		if key in self.data:
			self.queue.remove(self.data[key])

		self.data[key] = self.queue.add(key, value)
