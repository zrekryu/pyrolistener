# PyroListener

Inline update listening for Pyrogram.

PyroListener lets you wait for Telegram updates directly inside your update handler's callback.

---

## Installation

```bash
pip install git+https://github.com/Zrekryu/pyrolistener.git
```

---


## Community

- 📢 News & Updates: [link](https://t.me/PyroListener)
- 💬 Discussion & Support: [link](https://t.me/PyroListenerChat)

## Setup

Register listeners once:

```python
from pyrogram import Client
from pyrolistener import ListenRegistry
from pyrolistener.handlers import MessageListenHandler, CallbackQueryListenHandler

app = Client("account")

listen_registry = ListenRegistry()

app.add_handler(MessageListenHandler(listen_registry))
app.add_handler(CallbackQueryListenHandler(listen_registry))
```

---

# Example

```python
from pyrogram import filters

from pyrolistener.exceptions import ListenTimeoutError
from pyrolistener.helpers.listen import listen_message

@app.on_message(filters.command("age"))
async def ask_age(client, message):
    await message.reply("What is your age?")

    try:
        response = await listen_message(
            listen_registry,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            filters=filters.regex(r"\d+"),
            timeout=10
        )
    except ListenTimeoutError:
        await message.reply("Timed out.")
        return

    await message.reply(f"Age: {response.message.text}")
```

## How it works

1. Listener handlers receive updates.
2. Matching requests are resolved.
3. Awaiting code resumes.

```
Update → Listener → Match → Response → await listen() resumes
```

## License 
MIT
