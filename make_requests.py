import requests
import logging
import time
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_delay, RetryCallState, RetryError as TenacityRetryError

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
	stop=stop_after_delay(60),
	retry_error_callback=on_failure_callback(logger),
	before_sleep=retry_with_log(logger),
)

external_ids = [
	4743467,4790936,4791907,4806102,5292745,5330237,5408151,6037815,6038416,6038423,6046138,6050008,6052680,6053117,6059720,6071258,6071381,6071755,
	6072946,6074018,6074540,6074624,6074839,6075836,6076285,6077022,6082778,6083169,6906789,6907590,6914529,6920117,6925676,6930021,6943284,6943697,
	7087238,7126881,7132670,7188976,7251585,7378150,7444307,7526964,7692855,7798599,7823445,7831616,7973189,7988746,8015426,8225722,8230055,8263494,
	8282175,8284801,8582108,8591175,8607355,8612166,8627423,8678364,8692231,8695590,8699008,8699591,8702426,8704593,8713014,8754566,8845637,8867584,
	8886658,8894352,8933791,8952865,8982939,8986181,8988244,9013982,9023434,9029363,9030790,9032240,9032432,9034179,9034491,9039973,9040985,9043781,
	9044280,9047944,9053702,9060040,9066765,9072716,9074717,9076591,9077587,9078104,9083255,9087782,9089607,9089708,9090479,9091961,9092221,9093427,
	9093675,9094295,9095073,9095846,9097915,9099646,9101680,9106106,9110794,9134641,9138532,9145168,9149863,9167253,9185931,9192327,9210992,9237690,
	9246279,9248174,9249194,9274177,9274979,9290217,9291740,9294094,9297151,9298799,9299750,9301345,9303611,9307235,9314769,9319562,9319868,9328786,
	9333348,9337801,9340075,9341462,9341559,9360390,9362415,9365227,9371091,9387785,9402162,9426731,9429976,9435736,9436480,9443362,9459791,9461721,
	9462778,9505523,9511208,9511619,9514783,9525410,9548249,9562352,9628159,9692602,9721345,9726340,9764897,9779070,9799302,9802350,9817912,9823810,
	9841464,9845935,9846665,9847852,9856763,9875117,9876329,9897774,9897922,9904672,9913921,9916638,9940793,9942727,9950770,9960110,9968292,9968377,
	9969830,10001479,10004263,10004554,10014491,10014824,10014954,10015083,10015751,10021909,10022095,10022139,10022187,10022357,10022408,10023366,
	10023638,10024088,10024271,10024291,10025695,10026001,10026309,10027662,10028069,10028200,10028255,10028269,10028729,10028930,10029528,10029590,
	10029677,10030689,10030981,10031084,10031531,10031735,10031893,10032230,10033574,10033767,10033824,10034000,10034339,10034655,10037489,10037494,
	10027552,10038202,10038266,10038711,10039274,10039568,10039754,10042472,10044365,10052483,10066536,10067685,10072706,10088485,10095378,10100441,
	10104482,10106095,10111045,10112331,10115500,10115519,10116839,10117089,10122154,10124379,10125456,10136829,10142447,10146485,10146825,10162122,
	10164763,10166878,10169640,10173916,10174312,10175515,10177810,10190611,10191887,10203918,10224542,10239832,10239926,10242034,10244464,10252870,
	10254359,10260344,
]

api_key = '...'
with_address = 0
start_time = time.time()

@retry_config
def do_request(external_id) -> requests.Response:
	return requests.get(f'https://TEST_API/{external_id}?api_key={api_key}')

for i, id in enumerate(external_ids, start=1):
	try:
		res = do_request(id)
		if res.status_code != 200:
			raise Exception(f'status code not 200; {res.text}')

		data = res.json()

	except Exception as e:
		logger.error(repr(e))
		continue

	address = None
	if 'address' in data:
		address = data['address']

	if address is not None:
		logger.info(f'subscription with external_id {id} has address: {repr(address)}')
		with_address += 1

	if address is None and ('id' not in data or int(data['id']) != id):
		logger.debug(data)

	if i % 10 == 0:
		elapsed_seconds = time.time() - start_time

		if elapsed_seconds < 60:
			sleep_time = 60 - elapsed_seconds

			logger.info(f'sleeping for {sleep_time} seconds to throttle requests')
			time.sleep(sleep_time)

			start_time = time.time()

logger.info(f'Finished! Found {with_address} subs with address and {len(external_ids) - with_address} subs without address')
