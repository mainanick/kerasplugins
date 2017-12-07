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

import unittest

from kerasplugins import callbacks
from kerasplugins import exceptions


class TestKerasPlugins(unittest.TestCase):

    def test_cannot_init_with_invalid_event_type(self):
        with self.assertRaises(exceptions.CallbackException):
            telegram = callbacks.TelegramNotify(0, 0, msg="msg", notify="")

    def tests_event_can_be_notified(self):
        notify = {
            'on_batch_begin',
            # 'on_batch_end',
            'on_epoch_begin',
            'on_epoch_end',
            'on_train_begin',
            # 'on_train_end'
        }

        telegram = callbacks.TelegramNotify(0, 0, msg="msg", notify=notify)

        self.assertTrue(telegram.notify_train_begin)
        self.assertTrue(telegram.notify_batch_begin)
        self.assertTrue(telegram.notify_epoch_begin)
        self.assertTrue(telegram.notify_epoch_end)

        self.assertFalse(telegram.notify_train_end)
        self.assertFalse(telegram.notify_batch_end)
