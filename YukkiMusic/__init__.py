from pyrogram import Client, filters
from config import *
from pytgcalls import PyTgCalls



bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="YukkiMusic.plugins"),
)

app = Client(
    name="Assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
)


call = PyTgCalls(app)
