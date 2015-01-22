#!/usr/bin/python

from flask import Flask
from flask import request

import requests
import json

app = Flask(__name__)


class WebhookReceiver(object):

    plugins = []

    def send_events(self, event):
        for plugin in self.plugins:
            plugin().output(event)

    @classmethod
    def plugin(cls, plugin):
        cls.plugins.append(plugin)

    @app.route('/', methods=['POST'])
    def receive_hook(self):
        payload = json.loads(request.data)
        self.send_events(payload)


@WebhookReceiver.plugin
class StdoutOutput(object):

    def output(self, event):
        print event


# @WebhookReceiver.plugin
class ElasticsearchOutput(object):

    def __init__(self, es_host, es_index, es_type):
        self.es_host = es_host
        self.es_index = es_index
        self.es_url = "http://{es_host}/{es_index}/{es_type}".format(
            es_host=self.es_host,
            es_index=self.es_index,
            es_type=self.es_type)

    def output(self, event):
        requests.put(self.es_url, payload=event)

if __name__ == '__main__':
    app.run()
