from typing import List

def isValid(s: str) -> bool:
	close_chars = {']', ')', '}'}
	close_char_map = {'[': ']', '(': ')', '{': '}'}

	stack = []
	for char in s:
		if char in close_chars:
			if not stack or close_char_map[stack.pop()] != char:
				return False

		else:
			stack.append(char)

	return not stack

def generateParenthesis(n: int) -> List[str]:
	length = n * 2
	combinations = []

	def add_char(text: str, opens: int, closes: int):
		if opens + closes == length:
			combinations.append(text)
			return

		if opens < n:
			add_char(text + '(', opens+1, closes)

		if closes < opens:
			add_char(text + ')', opens, closes+1)

	add_char('', 0, 0)
	return combinations
