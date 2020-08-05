from typing import Union

import configparser as _configparser
import datadog as _datadog


def _get_datadog_secrets():
    parser = _configparser.ConfigParser()
    parser.read("config.ini")
    api_key = parser["DEFAULT"]["dd_api_key"]

    return api_key


def post_watt_usage(
    watts: Union[float, int, str], metric_name: str = "coffeegrinder.watts.usage"
):
    """ Post watts usage to datadog with given metric name """

    dd_api_key = _get_datadog_secrets()

    options = {
        "api_key": dd_api_key,
        ## EU costumers need to define 'api_host' as below
        "api_host": "https://api.datadoghq.eu/",
    }
    _datadog.initialize(**options)

    _datadog.api.Metric.send(metric=metric_name, points=watts)
