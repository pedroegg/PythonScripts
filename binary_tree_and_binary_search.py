from typing import List, Optional, Self, Union

class TreeNode:
	def __init__(self, val: int = 0, left: Union[Self, None] = None, right: Union[Self, None] = None):
		self.val = val
		self.left = left
		self.right = right

def search(nums: List[int], target: int) -> int:
	pos = len(nums) // 2

	offset = 0
	while nums:
		number = nums[pos]

		if number == target:
			return offset + pos

		if target > number:
			nums = nums[pos+1:]
			offset += pos + 1

		else:
			nums = nums[:pos]

		pos = len(nums) // 2

	return -1

def firstBadVersion(n: int) -> int:
	#mock
	def isBadVersion(version: int) -> bool:
		pass

	offset = 0
	bad_version = 0

	while n > 0:
		current = n // 2
		version = offset + current + 1

		if not isBadVersion(version):
			steps_to_move = current + 1
			n -= steps_to_move
			offset += steps_to_move

		else:
			n = current
			bad_version = version

	return bad_version

def sortedArrayToBST(nums: List[int]) -> Optional[TreeNode]:
	n = len(nums)
	if n == 0:
		return None

	middle = n // 2
	head = TreeNode(nums[middle], nums[:middle], nums[middle+1:])

	def createNodes(current: TreeNode):
		if not current.left:
			current.left = None

		if not current.right:
			current.right = None

		if current.left:
			left_i = len(current.left) // 2
			current.left = TreeNode(
				current.left[left_i],
				current.left[:left_i],
				current.left[left_i+1:]
			)

			createNodes(current.left)

		if current.right:
			right_i = len(current.right) // 2
			current.right = TreeNode(
				current.right[right_i],
				current.right[:right_i],
				current.right[right_i+1:]
			)

			createNodes(current.right)

	createNodes(head)
	return head

def sortedArrayToBST_V2(nums: List[int]) -> Optional[TreeNode]:
	n = len(nums)
	if n == 0:
		return None

	middle = n // 2
	node = TreeNode(nums[middle])
	node.left = sortedArrayToBST_V2(nums[:middle])
	node.right = sortedArrayToBST_V2(nums[middle+1:])

	return node

def isBalanced(root: Optional[TreeNode]) -> bool:
	if not root:
		return True

	def check(node: TreeNode):
		dl = dr = 0
		ok_l = ok_r = True

		if node.left:
			ok_l, dl = check(node.left)

		if node.right:
			ok_r, dr = check(node.right)

		ok = abs(dl - dr) <= 1 and ok_l and ok_r
		depth = 1 + max(dl, dr)

		return ok, depth

	return check(root)[0]

#não funciona pra solução ótima porque não permite skippar mais de um nó por vez
def rob(root: Optional[TreeNode]) -> int:
	if not root:
		return 0

	def walk(node: TreeNode, get: bool) -> int:
		total = 0

		if node and get:
			total += node.val

		if node.left:
			total += walk(node.left, not get)

		if node.right:
			total += walk(node.right, not get)

		return total

	sum_1 = walk(root, True)
	sum_2 = walk(root, False)

	return max(sum_1, sum_2)

#solução correta com solução ótima
def robV2(root: Optional[TreeNode]) -> int:
	if not root:
		return 0

	def dfs(node: TreeNode):
		if not node:
			return 0, 0

		robbing_left, skipping_left = dfs(node.left)
		robbing_right, skipping_right = dfs(node.right)

		robbing = node.val + skipping_left + skipping_right
		skipping = max(robbing_left, skipping_left) + max(robbing_right, skipping_right)

		return robbing, skipping

	return max(dfs(root))
