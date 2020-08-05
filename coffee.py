#! /usr/bin/env python3
"""
Post coffee messages to slack!

Requires `slackclient` python-library
"""
from typing import List, Optional

import argparse as _argparse
import configparser as _configparser
import logging as _logging

_logger = _logging.getLogger(__name__)

try:
    import slack as _slack
except (ModuleNotFoundError, ImportError):
    import sys as _sys

    _logger.error(
        "Can not import `slack` library - do you need to do a `pip install slackclient` first?",
    )
    _sys.exit()


def _create_header_block(header: str) -> dict:
    return {
        "type": "header",
        "text": {"type": "plain_text", "text": header, "emoji": True},
    }


def _create_message_block(message: str) -> dict:
    """ Creates message block -- supports mrkdwn! """
    return {
        "type": "section",
        "text": {"type": "mrkdwn", "text": message,},
    }


def _fill_message_template(header: str, message: Optional[str] = None) -> List[dict]:
    """ Fill necessary dictionary for JSON to send to slack; `header` supports emojis - `message` supports mrkdwn """
    header = _create_header_block(header)

    _message_block = None
    if message:
        _message_block = _create_message_block(message)

    blocks = list(filter(None, (header, _message_block)))

    return blocks


def _get_token() -> str:
    parser = _configparser.ConfigParser()
    parser.read("config.ini")
    return parser["DEFAULT"]["slack_token"]


def _slack_client() -> _slack.WebClient:
    bot_token = _get_token()
    return _slack.WebClient(token=bot_token)


def post_it(
    header: str = "Somebody is brewing delicious hot coffee! ☕",
    message: Optional[str] = None,
    channel: str = "shipit-coffee-machine",
):
    """ Post `message` with given `header` to slack """
    blocks = _fill_message_template(header, message)
    client = _slack_client()
    client.chat_postMessage(channel=channel, blocks=blocks)


if __name__ == "__main__":
    # execute only if run as a script
    parser = _argparse.ArgumentParser()
    parser.add_argument(
        "--header", type=str, default="Somebody is brewing delicious hot coffee! ☕"
    )
    parser.add_argument("--message", type=str)

    args = parser.parse_args()
    post_it(header=args.header, message=args.message)
