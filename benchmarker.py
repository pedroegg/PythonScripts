import time
import string
import random
from functools import partial, cache
from typing import List, Tuple, Optional, Union, Any, Callable

EXECUTIONS_NUMBER = 50000

# ------------ UTILS ------------

class NOT_SET:
	pass

class Generator():
	def __init__(self, func: Callable, expected: Optional[Callable[[Any], Any]] = None):
		self.f = func
		self.expected = expected

def random_int(min: int = 100, max: int = 1000) -> int:
	return random.randint(min, max)

def random_string(min_length: int = 100, max_length: int = 1000) -> str:
	length = random_int(min_length, max_length)

	chars = string.ascii_letters + string.digits + string.punctuation + " "
	return ''.join(random.choice(chars) for _ in range(length))

def random_range(min: int = 100, max: int = 1000) -> range:
	return range(random_int(min, max))

def random_string_not_palindrome(min_length: int = 100, max_length: int = 1000) -> str:
	length = random_int(min_length, max_length)

	chars = string.ascii_letters + string.digits + string.punctuation + " "
	half_len = length // 2
	first_half = [random.choice(chars) for _ in range(half_len)]
	second_half = [random.choice(chars) for _ in range(half_len)]

	middle = [random.choice(chars)] if length % 2 else []

	if half_len > 0 and first_half[0] == second_half[-1]:
		available_chars = chars.replace(first_half[0], '')
		second_half[-1] = random.choice(available_chars)

	return ''.join(first_half + middle + second_half[::-1])

def random_palindrome(min_length: int = 100, max_length: int = 1000) -> str:
	length = random_int(min_length, max_length)

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

def dataset_maker(generators: List[Generator]) -> Callable[[int], List[Tuple[Any, Union[Any, NOT_SET]]]]:
	@cache
	def maker(size: int) -> List[Tuple[Any, Optional[Any]]]:
		num_generators = len(generators)
		if num_generators == 0:
			return []

		cuts = sorted(random.sample(range(1, size), num_generators - 1)) if num_generators > 1 else []
		counts = [end - start for end, start in zip(cuts + [size], [0] + cuts)]

		return random.sample(
			[
				(
					gen_input := generator.f(),
					generator.expected(gen_input) if generator.expected is not None else NOT_SET()
				) for generator, count in zip(generators, counts)
					for _ in range(count)
			],
			size,
		)

	return maker

def attach_dataset_generator(dataset_generator: Callable[[int], List[Tuple[Any, Union[Any, NOT_SET]]]]) -> Callable:
	def decorator(func):
		func.dataset_generator = dataset_generator
		return func
	return decorator

# ------------------------------------

# ------------ DATASETS ------------

class DatasetGenerator:
	palindrome = dataset_maker(
		[
			Generator(func=partial(random_palindrome, min_length=500, max_length=5000), expected=lambda _: True),
			Generator(func=partial(random_string_not_palindrome, min_length=500, max_length=5000), expected=lambda _: False),
		]
	)

	reverse_str = dataset_maker([Generator(func=partial(random_string, max_length=10000))])

	sum = dataset_maker([Generator(func=partial(random_range, min=1000, max=10000))])

	iter = dataset_maker([Generator(func=partial(random_range, min=1000, max=10000))])

# ------------------------------------

# ------------ TEST FUNCS ------------

@attach_dataset_generator(DatasetGenerator.reverse_str)
def reverse_str_pythonic(s: str) -> str:
	return s[::-1]

@attach_dataset_generator(DatasetGenerator.reverse_str)
def reverse_str_reversed_join(s: str) -> str:
	return ''.join(reversed(s))

@attach_dataset_generator(DatasetGenerator.reverse_str)
def reverse_str_reversed_iter(s: str) -> str:
	res = ''
	for c in reversed(s):
		res += c

	return res

@attach_dataset_generator(DatasetGenerator.reverse_str)
def reverse_str_join_iter(s: str) -> str:
	return ''.join(s[i] for i in range(len(s)-1, -1, -1))

@attach_dataset_generator(DatasetGenerator.reverse_str)
def reverse_str_iter(s: str) -> str:
	res = ''
	for i in range(len(s)-1, -1, -1):
		res += s[i]

	return res

@attach_dataset_generator(DatasetGenerator.sum)
def sum_iter(r: range) -> int:
	s = 0
	for i in r:
		s += i

	return s

@attach_dataset_generator(DatasetGenerator.sum)
def sum_gen(r: range) -> int:
	return sum(i for i in r)

@attach_dataset_generator(DatasetGenerator.iter)
def iter(r: range) -> None:
	for _ in r:
		pass

@attach_dataset_generator(DatasetGenerator.iter)
def iter_generator(r: range) -> None:
	for _ in (_ for _ in r):
		pass

@attach_dataset_generator(DatasetGenerator.palindrome)
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

@attach_dataset_generator(DatasetGenerator.palindrome)
def isPalindromeV2(s: str) -> bool:
	new_string = [char for char in s.lower() if char.isalnum()]
	return new_string == new_string[::-1]

# ------------------------------------

# ------------ TEST HELPER ------------

def get_func_name(func: Callable) -> str:
	return getattr(func, '__name__', 'None')

def do_benchmark(func: Callable, executions_number: int) -> Tuple[float, float, List[Union[bool, None]], None]:
	dataset = None
	if hasattr(func, 'dataset_generator'):
		dataset: List[Tuple[Any, Union[Any, NOT_SET]]] = func.dataset_generator(size=executions_number)

	results: List[Union[bool, None]] = []
	start = time.perf_counter()

	if dataset is not None:
		for gen_input, expected_output in dataset:
			output = func(gen_input)

			ok = None
			if not isinstance(expected_output, NOT_SET):
				ok = output == expected_output

			results.append(ok)

	else:
		for _ in range(executions_number):
			func()

	elapsed = time.perf_counter() - start
	average = elapsed / executions_number

	return elapsed, average, results

# ------------------------------------

class Test():
	def __init__(self, func: Callable, executions_number: Optional[int] = EXECUTIONS_NUMBER):
		self.func = func
		self.executions_number = executions_number

tests: List[Test] = [
	Test(reverse_str_pythonic),
	Test(reverse_str_reversed_join),
	Test(reverse_str_reversed_iter),
	Test(reverse_str_join_iter),
	Test(reverse_str_iter),
	Test(sum_iter),
	Test(sum_gen),
	Test(iter),
	Test(iter_generator),
	Test(isPalindrome),
	Test(isPalindromeV2),
]

for t in tests:
	elapsed, average, results = do_benchmark(t.func, t.executions_number)
	hits = [1 if result else 0 for result in results if result is not None]

	precision_str = ''
	if len(hits) > 0:
		precision_str = f'Precision: {(sum(hits) / len(results)) * 100:.2f}%\n'

	print(
		f'Function: {get_func_name(t.func)}\n'
		f'Total: {elapsed:.6f} seconds\n'
		f'Average: {average:.6f} seconds\n'
		f'{precision_str}'
	)
