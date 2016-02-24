"""
TODO: docs
"""

from .channel import Channel
from .constants import CHANNEL_BASE_URL


# TODO: Move this into a threading.local object
_session_stack = []

class Session(object):

    def __init__(self, session_id, program):
        self.session_id = session_id
        self.program = program
        self.client_channel = Channel(CHANNEL_BASE_URL, session_id)

    def __enter__(self):
        _session_stack.append(self)
        return self

    def __exit__(self, type, value, traceback):
        removed = _session_stack.pop()
        if removed != self:
            raise ValueError('Stack consistency mismatch: {} vs. {}'.format(
                removed.session_id,
                self.session_id
            ))

    def send(self, msg):
        self.client_channel.enqueue(msg)

    def set(self, key, value):
        pass

    def get(self, key):
        pass


def session():
    if len(_session_stack) == 0:
        raise ValueError("Attempted to call session() without a running program.")
    return _session_stack[-1]