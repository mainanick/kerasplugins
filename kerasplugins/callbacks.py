import requests
import telegram
from keras.callbacks import Callback


class TelegramNotify(Callback):
    def __init__(self, token, chat_id, msg=None, notify={}):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id
        self.init_msg = msg or "model starting to train"

        self.notify_train_begin = 'on_train_begin' in notify
        self.notify_train_end = 'on_train_end' in notify

        self.notify_batch_begin = 'on_batch_begin' in notify
        self.notify_batch_end = 'on_batch_end' in notify

        self.notify_epoch_begin = 'on_epoch_begin' in notify
        self.notify_epoch_end = 'on_epoch_end' in notify

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
    
    def notify(self, logs={}, msg=None, level=""):
        acc = logs.get('loss', "")  
        loss = logs.get('acc', "")

        try:        
            text = msg or "{}: Loss {} Accuracy {}".format(level, loss, acc)
            self.bot.send_message(chat_id=self.chat_id,text=text)        
        
        except Exception as e:
            pass
