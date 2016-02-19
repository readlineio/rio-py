from channel import Channel
import json
import random
import threading

key = None

STAGE = 'development'
server_name = 'localhost:8080'
channel_base = 'http://localhost:8888'

# TODO: hardcoded host parameter
channel = Channel('http://readline.io', 'index')

application_main = None

# TODO: again, global here? is this safe?
session_stack = []

# TODO: globals???
registered_callbacks = {}


def register_callback(callback):
    key = callback.__module__ + '.' + callback.__name__
    registered_callbacks[key] = callback
    return key


class SessionContext(object):

    def __init__(self, session_id):
        self.session_id = session_id
        self.channel = Channel(channel_base, session_id)
        self.client_channel = Channel(channel_base, session_id)

    def __enter__(self):
        session_stack.append(self)

    def __exit__(self, type, value, traceback):
        removed = session_stack.pop()
        if removed != self:
            raise ValueError('Stack consistency mismatch: {} vs. {}'.format(removed.session_id, self.session_id))

    def send(self, msg):
        self.client_channel.enqueue(msg)


class DeferredInput(object):

    def __init__(self, session, prompt):
        self.session = session
        self.prompt = prompt

    def then(self, callback):
        callback_name = register_callback(callback)
        message = {
            'type': 'input',
            'prompt': self.prompt,
            'callback': callback_name
        }
        self.session.send(message)


class DeferredChoice(object):

    def __init__(self, session, prompt):
        self.session = session
        self.prompt = prompt

    def then(self, callback):
        callback_name = register_callback(callback)
        message = {
            'type': 'choice',
            'prompt': self.prompt,
            'callback': callback_name
        }
        self.session.send(message)


def session():
    return session_stack[-1]


def main(inner_f):
    # TODO: global? are you crazy?
    global application_main
    application_main = inner_f
    return inner_f


def output(text):
    # Write something to the current session's firebase
    send({
        'type': 'output',
        'text': text
    })


def output_image(url):
    send({
        'type': 'image',
        'url': url
    })


def send(message):
    sess = session()
    sess.send(message)


def input(text):
    # Write something to the current session's firebase
    return DeferredInput(session(), text)


def choice(text):
    return DeferredChoice(session(), text)


def handle_message(message):
    action = message.get('action')
    print('message action:', action)

    if action == 'start':
        session_id = message.get('session', 'TODO')
        with SessionContext(session_id):
            sess = session()
            application_main()

    elif action == 'call':
        session_id = message.get('session', 'TODO')
        with SessionContext(session_id):
            fnname, args, kwargs = message['fnname'], message['args'], message['kwargs']
            fn = registered_callbacks[fnname]
            fn(*args, **kwargs)
    else:
        print("The hell is this action:", action)


def random_page_id(length=10):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(chars) for _ in range(length))


def run():
    page_id = random_page_id()
    page_channel = Channel(channel_base, page_id)
    print("Access your application by going to http://{}/{}".format(server_name, page_id))
    while True:
        message = page_channel.dequeue()
        if message:
            # TODO: add proper logging here
            print("Message received: len={}".format(len(json.dumps(message))))
            handle_message(message)
        else:
            print("No message received, continuing long poll.")


def run_backgrounded():
    readline_thread = threading.Thread(target=run, daemon=True)
    readline_thread.start()
