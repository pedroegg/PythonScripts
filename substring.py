def substring_search_v1(text: str, substring: str) -> int:
	n = len(text)
	m = len(substring)

	if m > n or m == 0:
		return -1

	current_substring = ''
	for i, char in enumerate(text):
		current_substring += char

		if len(current_substring) == m:
			if current_substring == substring:
				return i - (m-1)

			current_substring = current_substring[1:]

	return -1

def substring_search_v2(text: str, substring: str) -> int:
	return text.find(substring)