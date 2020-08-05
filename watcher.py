#! /usr/bin/env python3
import subprocess as _subprocess
import json as _json
import decimal as _decimal
import datetime as _dt
import logging as _logging
import time as _time

import datadog as _datadog
import notify as _notify
import picture as _picture


_logger = _logging.getLogger(__name__)


def query_sem6000_status() -> dict:
    """ Query Voltcraft SEM6000 status

    Example response:
    {
      "device" : null,
      "status" : {
        "power" : 1,
        "voltage" : 227,
        "ampere" : 0.021,
        "watts" : 0.919,
        "frequency" : 50,
        "power_factor" : 0.19,
        "total" : 0.0
      },
      "settings" : null,
      "schedulers" : null,
      "countdown" : null,
      "randommode" : null,
      "data_per_hour" : [
      ],
      "data_per_day" : [
      ],
      "data_per_month" : [
      ]
    }
    """
    process = _subprocess.Popen(
        [
            "/home/pi/voltcraft-sem-6000/sem-6000.exp",
            "coffee_grinder",
            "--status",
            "--json",
        ],
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    return _json.loads(stdout)


def get_current_power_consumption() -> _decimal.Decimal:
    """ return current power consumption in watts """
    status_response = query_sem6000_status()
    return _decimal.Decimal(status_response["status"]["watts"])


if __name__ == "__main__":

    time_of_last_use = _dt.datetime(1970, 1, 1)

    while True:
        power_consumption = get_current_power_consumption()

        _logger.info("Using %r watts", power_consumption)
        if power_consumption > 10:
            time_since_last_use = _dt.datetime.now() - time_of_last_use

            if time_since_last_use > _dt.timedelta(minutes=10):
                _logger.info("SOMEONE IS MAKING COFFEE")

                image_filename = _picture.take_picture()
                _notify.post_it(message=image_filename)

            time_of_last_use = _dt.datetime.now()

        _datadog.post_watt_usage(power_consumption)
        _time.sleep(1)
