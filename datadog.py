import configparser as _configparser
import time as _time

import requests as _requests


def _get_datadog_secrets():
    parser = _configparser.ConfigParser()
    parser.read("config.ini")
    api_key = parser["DEFAULT"]["dd_api_key"]

    return api_key


def post_watt_usage(watts: float, metric_name: str = "coffee_grinder_watt_usage"):
    """ Post watts usage to datadog with given metric name """
    dd_api_key = _get_datadog_secrets()
    now = _time.time()

    headers = {
        "Content-Type": "application/json",
    }

    data = dict(series=[dict(metric=metric_name, points=[str(now), str(watts)])])

    resp = _requests.post(
        f"https://api.datadoghq.eu/api/v1/series?api_key={dd_api_key}",
        headers=headers,
        json=data,
    )

    resp.raise_for_status()
