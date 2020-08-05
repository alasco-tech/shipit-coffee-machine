#! /usr/bin/env python3
import datetime as _dt
import logging as _logging
import time as _time

import datadog_client as _datadog
import notify as _notify
import picture as _picture
import sem6000 as _sem6000


_logger = _logging.getLogger(__name__)


if __name__ == "__main__":

    time_of_last_use = _dt.datetime(1970, 1, 1)

    while True:
        power_consumption = _sem6000.get_current_power_consumption()

        _logger.warning("Using %r watts", power_consumption)
        if power_consumption > 10:
            time_since_last_use = _dt.datetime.now() - time_of_last_use

            if time_since_last_use > _dt.timedelta(minutes=10):
                _logger.warning("SOMEONE IS MAKING COFFEE")

                image_filename = _picture.take_picture()
                _notify.post_image(filename=image_filename)

            time_of_last_use = _dt.datetime.now()

        _datadog.post_watt_usage(power_consumption)
        _time.sleep(1)
