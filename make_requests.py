import requests
import logging
import time
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_delay, RetryCallState, RetryError as TenacityRetryError

from datetime import datetime
from zoneinfo import ZoneInfo
import json

from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger("Main")

class ExhaustedRetriesError(TenacityRetryError):
	def _safe_exception(self) -> BaseException:
		try:
			return self.last_attempt.exception()
		except:
			return Exception('Unknown error')

	def __str__(self) -> str:
		last_exc = self._safe_exception()
		return f'[RETRY FAILED] | Last exception: {type(last_exc).__name__}: {last_exc}'

	def __repr__(self) -> str:
		last_exc = self._safe_exception()

		return (
			f'{self.__class__.__name__}'
			'('
				f'attempts={self.last_attempt.attempt_number}, '
				f'final_exception={type(last_exc).__name__}'
			')'
		)

def on_failure_callback(logger: logging.Logger):
	def _callback(rs: RetryCallState):
		exc = ExhaustedRetriesError(last_attempt=rs.outcome)
		logger.warning(str(exc))

		raise exc

	return _callback

def retry_with_log(logger: logging.Logger):
	def _retry(rs: RetryCallState):
		e = rs.outcome.exception()

		attempt_number = rs.attempt_number

		stop_obj = getattr(rs.retry_object, "stop", None)
		total_attempts = getattr(stop_obj, "max_attempt_number", "inf") if stop_obj is not None else "inf"
		max_delay = getattr(stop_obj, "max_delay", None)

		current_attempt_msg = f'{attempt_number}/{total_attempts}'
		if max_delay is not None:
			elapsed = rs.idle_for
			current_attempt_msg = f'{elapsed:.1f}s/{int(max_delay)}s'

		next_sleep = getattr(rs.next_action, "sleep", None)

		next_retry_msg = 'Retrying now'
		if next_sleep is not None:
			next_retry_msg = f'Next in {next_sleep:.1f}s'

		logger.warning(
			f'[RETRY {current_attempt_msg}] | '
			f'{next_retry_msg} | '
			f'Error: {type(e).__name__}: {e}'
		)

	return _retry

retry_config = retry(
	retry=retry_if_exception_type(Exception),
	wait=wait_exponential(multiplier=1, min=1, max=30),
	stop=stop_after_delay(75),
	retry_error_callback=on_failure_callback(logger),
	before_sleep=retry_with_log(logger),
)

external_ids = [
	4791907, 5330237, 5408151, 6059720, 6071381, 6071755, 6072946, 6074540, 6074624, 6075836, 6076285, 6907590, 6920117,
	6943284, 6943697, 7823445, 7973189, 8284801, 8582108, 8612166, 8678364, 8699008, 8702426, 8704593, 8894352, 8982939,
	8986181, 9030790, 9034179, 9039973, 9043781, 9047944, 9060040, 9066765, 9077587, 9078104, 9083255, 9087782, 9094295,
	9095846, 9134641, 9192327, 9274177, 9290217, 9291740, 9297151, 9301345, 9319562, 9328786, 9340075, 9341462, 9435736,
	9462778, 9511208, 9511619, 9514783, 9562352, 9764897, 9897774, 9940793, 9968377, 10022187, 10022408, 10028069, 10028255,
	10028930, 10029677, 10030689, 10033574, 10034000, 10034655, 10039754, 10066536, 10067685, 10106095, 10116839, 10146485,
	10146825, 10239926, 10244464, 10252870, 10254359, 10260344,
]

api_key = '...'
max_reqs_per_interval = 10
interval_seconds = 60

@retry_config
def do_request(external_id) -> requests.Response:
	try:
		res = requests.post(f'https://api-name/path/{external_id}/cancel?api_key={api_key}')
		if res.status_code != 200:
			raise Exception(f'status code not 200; {res.text}')

		data = res.json()

	except:
		raise

	return data

emails = []

start_time = time.time()
for i, external_id in enumerate(external_ids, start=1):
	try:
		sub: Dict[str, Any] = do_request(external_id)

	except Exception as e:
		logger.error(repr(e))
		continue

	if 'customer' not in sub or 'email' not in sub['customer']:
		logger.info(f'sub with external_id {external_id} does not have an email or customer')
		continue

	emails.append(sub['customer']['email'])

	if i % max_reqs_per_interval == 0:
		elapsed_seconds = time.time() - start_time

		if elapsed_seconds < interval_seconds:
			sleep_time = interval_seconds - elapsed_seconds

			logger.info(f'sleeping for {sleep_time} seconds to throttle requests')
			time.sleep(sleep_time)

			start_time = time.time()

logger.info(f'Finished! {len(emails)} emails\n')
for email in emails:
	print(email)
