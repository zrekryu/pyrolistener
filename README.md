# PyroListener

Inline update listening for Pyrogram.

PyroListener lets you wait for Telegram updates directly inside your update handler's callback.

---

## Installation

```bash
pip install git+https://github.com/Zrekryu/pyrolistener.git
```

---

## Setup

Register listeners once:

```python
from pyrogram import Client
from pyrolistener import ListenRegistry
from pyrolistener.handlers import MessageListener, CallbackQueryListener

app = Client("account")

listen_registry = ListenRegistry()

app.add_handler(MessageListener(listen_registry))
app.add_handler(CallbackQueryListener(listen_registry))
```

---

# Example

```python
from pyrogram import filters

from pyrolister.exceptions import ListenTimeoutError
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
Update → Listener → Match → await continues
```

# License 
MIT
