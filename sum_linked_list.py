from typing import Self, Optional

class ListNode:
	def __init__(self, val: int = 0, next: Self = None):
		self.val = val
		self.next = next

def addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
	node_1, node_2 = l1, l2

	sum_head = ListNode()
	sum_node = sum_head
	rest = 0

	while sum_node:
		res = rest
		if node_1:
			res += node_1.val
			node_1 = node_1.next

		if node_2:
			res += node_2.val
			node_2 = node_2.next

		sum_node.val = res % 10
		rest = res // 10

		if node_1 or node_2 or rest > 0:
			sum_node.next = ListNode()

		sum_node = sum_node.next

	return sum_head
