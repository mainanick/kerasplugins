# kerasplugins 🤓
[![PyPI](https://img.shields.io/pypi/v/kerasplugins.svg)]()
[![PyPI](https://img.shields.io/pypi/l/kerasplugins.svg)]()

##### Installation

```
pip install kerasplugins
```

## Callbacks
### Notification Callback 📮 💬
Get notified as your Keras neural network models trains remotely

Send log messages to your telegram and slack channels. *more coming soon*

Notify levels available:
1) on_train_begin,
2) on_train_end,
3) on_batch_begin,
4) on_batch_end,
5) on_epoch_begin,
6) on_epoch_end


```python
from kerasplugins import callbacks

#Notify can either be a list, dict or set
notify = { 
  'on_batch_end',  # sends BATCH END: Loss 0.50 Accuracy: 0.75
  'on_epoch_end'   # sends EPOCH END: Loss 0.43 Accuracy: 0.81
}

# msg is the initial message
msg = "Predicting Bitcoin Price"

telegram = callbacks.TelegramNotify(<token>, <chat_id>, msg=msg, notify=notify)

# channel is "#general" by default
slack = callbacks.SlackNotify(<slack_token>, <channel>, msg=msg, notify=notify)

webhook = callbacks.WebhookNotify('https://example.com/ml')

# Optionals:
#Headers default to "application/json"
headers = {'Content-Type': 'text/plain'}

# Added to every payload sent to the webhook
data = {"auth_token":"cccxxxvvvbbbnnnmmmaaasss"}

webhook = callbacks.WebhookNotify('https://example.com/ml', data=data, headers=headers)

model.fit(X_train, Y_train, validation_data=[X_test, Y_test], batch_size=256, epochs=10,
        callbacks=[telegram, slack, webhook])
```

## Coming Soon
1) Ability to stop training remotely
