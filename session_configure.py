import os
from pyrogram import Client

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
app = Client(
    "teraBox-Bypass",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token,
)
try:
    app.start()
    print(app.export_session_string())
finally:
    app.stop()
