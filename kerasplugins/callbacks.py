# Copyright (c) 2017 Maina Nick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import json
import warnings

import requests
import telegram
import slacker
from keras.callbacks import Callback
from . import exceptions


class PluginCallbacks(Callback):
    def __init__(self, msg=None, notify={}):
        # The initial message to be sent when model training begins
        self.init_msg = msg or "model starting to train"

        if not isinstance(notify, (list, dict, set)):
            raise exceptions.CallbackException(
                "Expected list, dict or set got {}".format(type(notify)))

        # Ensure notify_event is a O(1) access_time DS
        notify_event = set(notify) if isinstance(notify, list) else notify

        self.notify_train_begin = 'on_train_begin' in notify_event
        self.notify_train_end = 'on_train_end' in notify_event

        self.notify_batch_begin = 'on_batch_begin' in notify_event
        self.notify_batch_end = 'on_batch_end' in notify_event

        self.notify_epoch_begin = 'on_epoch_begin' in notify_event
        self.notify_epoch_end = 'on_epoch_end' in notify_event

        super()

    def on_train_begin(self, logs={}):
        if self.notify_train_begin:
            self.notify(msg=self.init_msg, level="TRAIN BEGIN")
            del self.init_msg

    def on_train_end(self, logs=None):
        if self.notify_train_end:
            self.notify(logs, level="TRAIN END")

    def on_batch_begin(self, batch, logs=None):
        if self.notify_batch_begin:
            self.notify(logs, level="BATCH BEGIN")

    def on_batch_end(self, batch, logs=None):
        if self.notify_batch_end:
            self.notify(logs, level="BATCH END")

    def on_epoch_begin(self, epoch, logs=None):
        if self.notify_epoch_begin:
            self.notify(logs, level="EPOCH BEGIN")

    def on_epoch_end(self, epoch, logs={}):
        if self.notify_epoch_end:
            self.notify(logs, level="EPOCH END")

    def notify(self):
        raise NotImplementedError


class TelegramNotify(PluginCallbacks):
    def __init__(self, token, chat_id, msg=None, notify={}):

        self.bot = None
        self.chat_id = chat_id
        self.token = token
        super().__init__(msg, notify)

    def notify(self, logs={}, msg=None, level=""):
        if self.bot is None:
            self.bot = telegram.Bot(token=self.token)

        acc = logs.get('loss', "")
        loss = logs.get('acc', "")

        try:
            text = msg or "{}: Loss {} Accuracy {}".format(level, loss, acc)
            self.bot.send_message(chat_id=self.chat_id, text=text)

        except Exception as e:
            warnings.warn(
                'Failed Notify Telegram Channel. Error {}'.format(str(e)))


class SlackNotify(PluginCallbacks):
    def __init__(self, slack_token, channel="#general", msg=None, notify={}):
        self.channel = channel
        self.token = slack_token
        self.slack = None

        super().__init__(msg, notify)

    def notify(self, logs={}, msg=None, level=""):
        if self.slack is None:
            self.slack = slacker.Slacker(self.token)

        acc = logs.get('loss', "")
        loss = logs.get('acc', "")

        try:
            text = msg or "{}: Loss {} Accuracy {}".format(level, loss, acc)
            self.slack.chat.post_message(self.channel, text)

        except Exception as e:
            warnings.warn(
                'Failed Notify Slack Channel. Error {}'.format(str(e)))


class WebhookNotify(PluginCallbacks):
    def __init__(self, url, headers=None, msg=None, notify={}):
        self.url = url
        self.headers = headers or {'Content-Type': 'application/json'}

        super().__init__(msg, notify)

    def notify(self, logs={}, msg=None, level=""):
        data = {k: v for k, v in logs.items()}

        try:
            requests.post(url, data=json.dumps(data), headers=self.headers)
        except requests.exceptions.RequestException as e:
            warnings.warn('Failed to reach server error {}'.format(str(e)))
