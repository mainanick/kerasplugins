# keras-plugins

## Telegram Callback

Notify levels available:
1) on_train_begin,
2) on_train_end,
3) on_batch_begin,
4) on_batch_end,
5) on_epoch_begin,
6) on_epoch_end
  
### How to use

```python
import callbacks

notify = { 
  'on_batch_end':True, 
  'on_epoch_end':True 
}


telegram = callbacks.TelegramNotify(<token>, <chat_id>, msg=msg, notify=notify)

model.fit(X_train, Y_train, validation_data=[X_test, Y_test], batch_size=256, epochs=10, callbacks=[telegram])
```
