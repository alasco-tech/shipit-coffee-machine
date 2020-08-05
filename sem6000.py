#! /usr/bin/env python3
import subprocess as _subprocess
import json as _json

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

    if "Connection failed" in str(stderr):
        _subprocess.Popen(["sudo", "reboot"])

    return _json.loads(stdout)


def get_current_power_consumption() -> float:
    """ return current power consumption in watts """
    status_response = query_sem6000_status()
    return float(status_response["status"]["watts"])