from datetime import datetime
from loguru import logger


class RandomTimeouts:
    _random = __import__("random")
    _time = __import__("time")

    def __init__(self, debug: bool = False):
        self.debug = debug

    def sleep_in_range(self, a: int, b: int, message: str = ""):
        random_time = (self._random.randint(a*10, b*10) / 10)
        time_to_end_sleep = (
            f"{datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%H:%M:%S.%f')}/ "
            f"{datetime.fromtimestamp(datetime.timestamp(datetime.now()) + random_time).strftime('%H:%M:%S.%f')}"
        )

        if self.debug: logger.opt(colors=True).debug(f"{message} <yellow>-</yellow> sleep {random_time}s | {time_to_end_sleep}")
        self._time.sleep(random_time)

    def sleep_by_number(self, i: int, message: str = ""):
        if i == 0: return
        self.sleep_in_range(i-1, i+1, message)
