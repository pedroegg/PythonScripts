def isPalindrome(n: int) -> bool:
	if n < 0:
		return False

	if n < 10:
		return True

	digits = []
	while n > 0:
		digits.append(n % 10)
		n = n // 10

	i, j = 0, len(digits)-1
	while i < j:
		if digits[i] != digits[j]:
			return False

		i += 1
		j -= 1

	return True
