from typing import List, Dict, Tuple

import math

def findDuplicate(nums: List[int]) -> int:
	slow = nums[0]
	fast = nums[nums[0]]

	while fast != slow:
		slow = nums[slow]
		fast = nums[nums[fast]]

	slow = 0
	while fast != slow:
		slow = nums[slow]
		fast = nums[fast]

	return slow

def findDuplicateV2(nums: List[int]) -> int:
	number = 0
	for n in nums:
		base = 10
		if n > 9:
			base = 10 ** (int(math.log10(abs(n))) + 1)

		number = (number * base) + n

	mask = 0
	while number > 0:
		digit = number % 10
		bit_to_insert = 1 << digit

		if mask & bit_to_insert:
			return digit

		mask = mask | bit_to_insert
		number = number // 10

	return -1

def findDuplicateV3(nums: List[int]) -> int:
	def next_position(index: int) -> int:
		return nums[index]

	slow = next_position(0)
	fast = next_position(next_position(0))
	while fast != slow:
		slow = next_position(slow)
		fast = next_position(next_position(fast))

	slow = next_position(slow)
	c = 1
	while fast != slow:
		slow = next_position(slow)
		c += 1

	fast = next_position(0)
	steps = 0
	while steps != c:
		fast = next_position(fast)
		steps += 1

	slow = next_position(0)
	while fast != slow:
		slow = next_position(slow)
		fast = next_position(fast)

	return slow

test_input = [3,1,3,4,2]
# 0 -> 3 -> 4 -> 2 -> ... (3,4,2)

print(f'Retorno: {findDuplicate(test_input)}')
print(f'Retorno v2: {findDuplicateV2(test_input)}')
print(f'Retorno v3: {findDuplicateV3(test_input)}')
