from collections import deque
from typing import Optional, Self

class ListNode:
	def __init__(self, val: int = 0, next: Self = None):
		self.val = val
		self.next = next

#não duplica memória mas dá pra melhorar
def rotateRight(head: Optional[ListNode], k: int) -> Optional[ListNode]:
	if not head:
		return None

	node = head
	n = 0
	while node:
		n += 1
		node = node.next

	k = k % n
	if k == 0:
		return head

	replacer_node = head
	queue = deque()
	steps = 0
	while steps < k:
		queue.append(replacer_node.val)
		replacer_node = replacer_node.next
		steps += 1

	start = replacer_node
	while replacer_node.next != start:
		queue.append(replacer_node.val)
		replacer_node.val = queue.popleft()

		replacer_node = replacer_node.next
		if not replacer_node:
			replacer_node = head

	replacer_node.val = queue.popleft()
	return head

#uso de memória duplicada
def rotateRightV2(head: Optional[ListNode], k: int) -> Optional[ListNode]:
	if not head:
		return None

	node = head
	queue = deque()
	while node:
		queue.append(node.val)
		node = node.next

	node = head
	queue.rotate(k)
	while queue:
		node.val = queue.popleft()
		node = node.next

	return

#não usa memória, é rápido e simples
def rotateRightV3(head: Optional[ListNode], k: int) -> Optional[ListNode]:
	if not head or not head.next or k == 0:
		return head

	tail = head
	n = 1
	while tail.next:
		tail = tail.next
		n += 1

	k = k % n
	if k == 0:
		return head

	tail.next = head

	new_tail = head
	for _ in range(n - k - 1):
		new_tail = new_tail.next

	new_head = new_tail.next
	new_tail.next = None

	return new_head
