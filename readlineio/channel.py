import requests
import json
import os.path


class Channel(object):

    def __init__(self, hostname, channel_id):
        self.hostname = hostname
        self.channel_id = channel_id
        self.url = os.path.join(hostname, 'channel', channel_id)

    def dequeue(self, timeout=50):
        # TODO: this needs to be able to handle multiplexing
        # possible use tornado async http / asyncio?
        try:
            resp = requests.get(self.url, timeout=timeout)
        except requests.exceptions.ReadTimeout:
            return None
        if resp.status_code == 200 and resp.text:
            return json.loads(resp.text)
        else:
            return None

    def enqueue(self, message):
        print("Sending message to client:", message)
        requests.post(self.url, data=json.dumps(message))