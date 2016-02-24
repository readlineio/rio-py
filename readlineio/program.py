"""
TODO: docs
"""

import os
import functools
import requests
import json
import random

from .channel import Channel
from .session import Session
from .constants import CHANNEL_BASE_URL, APPLICATION_BASE_URL


def random_page_id(length=10):
    chars = 'abcdef0123456789'
    return ''.join(random.choice(chars) for _ in range(length))


class Program(object):

    def __init__(self, main_function, title=None, debug=False):
        self.page_id = random_page_id()
        self.main_function = main_function
        self.title = title
        self.channel = Channel(CHANNEL_BASE_URL, self.page_id)
        self.callbacks = {}
        self.debug = debug
        self.__name__ = main_function.__name__
        self.__doc__ = main_function.__doc__

    def log(self, *messages):
        if self.debug:
            print(*messages)

    def url(self):
        return os.path.join(APPLICATION_BASE_URL, self.page_id)

    def register_callback(self, callback):
        key = callback.__module__ + '.' + callback.__name__
        self.callbacks[key] = callback
        return key

    def send_ping(self):
        message = {
            'page_id': self.page_id,
            'title': self.title
        }
        requests.post(
            os.path.join(CHANNEL_BASE_URL, 'program', 'register'),
            data=json.dumps(message)
        )
        # TODO: error handling here on HTTP error code != 200

    def handle_message(self, message):
        action = message.get('action')
        session_id = message['session']
        # TODO: handle invalid input

        self.log('Message action received:', action)

        with Session(session_id, program=self) as session:
            if action == 'start':
                session.send({
                    'type': 'title',
                    'text': self.title
                })
                self.main_function()

            elif action == 'call':
                fnname, args, kwargs = message['fnname'], message['args'], message['kwargs']
                fn = self.callbacks[fnname] # TODO: scoping is weird here
                fn(*args, **kwargs)

            else:
                self.log("Unknown action received:", action)

    def dequeue_and_handle_next_message(self):
        message = self.channel.dequeue()
        if message:
            self.log("Message received: len={}".format(len(json.dumps(message))))
            self.handle_message(message)
        else:
            self.log("No message received, continuing long poll.")

    def __call__(self, *args, **kwargs):
        self.main_function(*args, **kwargs)
