import threading

from .session import session
from .program import Program

key = None
stage = 'development'


# TODO: Move these actions into their own module?

class DeferredSend(object):

    def __init__(self, message=None):
        self.message = message.copy() or {}

    def then(self, callback):
        callback_name = session().program.register_callback(callback)
        self.message['callback'] = callback_name
        session().send(self.message)


def send(message):
    session().send(message)


def output(text):
    send({'type': 'output', 'text': text})


def output_image(url):
    send({'type': 'image', 'url': url})


def input(text):
    return DeferredSend({'type': 'input', 'prompt': text})


def choice(text):
    return DeferredSend({'type': 'choice', 'prompt': text})


def main(title):
    def make_inner(main_function):
        return Program(main_function=main_function, title=title)
    return make_inner


def run(program, debug=False):
    print("Access your application by going to {}".format(program.url()))
    program.debug = debug
    while True:
        program.send_ping()
        program.dequeue_and_handle_next_message()


def run_backgrounded():
    readline_thread = threading.Thread(target=run, daemon=True)
    readline_thread.start()
