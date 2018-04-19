import logging
from threading import Timer

try:
    from threading import _BoundedSemaphore as BoundedSemaphore
except ImportError:
    from threading import BoundedSemaphore
import time


class RatedSemaphore(BoundedSemaphore):
    """
    Limit to 1 request per `period / value` seconds (over long run). Used to put a limit on time-restricted resources.

    For instance, if we are allowed only 50 calls in 10 seconds to an API, you can use:

    ```
    semaphore = RatedSemaphore(50, 10)
    with semaphore:
        call_a_thing()
    ```

    This means we can call as fast as we like and only start blocking when we would exceed our limit.

    Copied with some modifications from:
    https://stackoverflow.com/a/16686329/489667
    """
    def __init__(self, value=1, period=1):
        """
        :param value: the number of tokens in a given period. This replenishes over time but blocks when it hits 0.
        :type value: int
        :param period: the time, in seconds, in a period
        :type period: int
        """
        super(RatedSemaphore, self).__init__(value)
        t = Timer(period, self._add_token_loop, kwargs={'time_delta': float(period) / value})
        t.daemon = True
        t.start()
        self.t = t

    def _add_token_loop(self, time_delta):
        """
        Add token every time_delta seconds.

        :param time_delta: the time between adding a token
        :type time_delta: float
        """
        while True:
            try:
                super(RatedSemaphore, self).release()
                try:
                    logging.debug("Rate Limiting: "
                                  "Requests remaining: %s; Replenishing every %s seconds.", self._value, time_delta)
                except AttributeError:
                    pass
            except ValueError:  # ignore if already max possible value
                pass
            time.sleep(time_delta)  # ignore EINTR

    def release(self):
        """
        Not allowed. Only the internal timer can call release.
        """
        pass  # called by the `with` statement so just ignore it
