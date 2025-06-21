import random
import string

def random_palindrome(length):
	half = [random.choice(string.ascii_letters + string.digits) for _ in range(length // 2)]
	middle = [random.choice(string.ascii_letters + string.digits)] if length % 2 else []
	pal = half + middle + half[::-1]
	num_noise = length // 5

	for _ in range(num_noise):
		idx = random.randint(0, (length-1)//2)
		noise = random.choice(string.punctuation + " ")
		pal[idx] = noise
		pal[-(idx+1)] = noise

	return ''.join(pal)

def isPalindrome(s: str) -> bool:
	s = s.lower()
	inverted_i = len(s)-1
	normal_i = 0

	while inverted_i > normal_i:
		i_char = s[inverted_i]
		if not i_char.isalnum():
			inverted_i -= 1
			continue

		n_char = s[normal_i]
		while not n_char.isalnum() and normal_i < inverted_i:
			normal_i += 1
			n_char = s[normal_i]

		if i_char != n_char:
			return False

		inverted_i -= 1
		normal_i += 1

	return True

def isPalindromeV2(s: str) -> bool:
	new_string = [char for char in s.lower() if char.isalnum()]
	return new_string == new_string[::-1]

palindrome = random_palindrome(10)
print(f'Generated palindrome: {palindrome}')

print(isPalindrome(palindrome))