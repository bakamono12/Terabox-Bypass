import asyncio
import os
from pyrogram import Client


async def main():
    api_id = os.environ.get('API_ID') or 1739665
    # api_id = 29810108
    api_hash = os.environ.get('API_HASH') or "467f5a7e96d1c78555e76aace5424b20"
    # api_hash = "a8b7762a934f12b7e519b6e4d56a1e37"

    app = Client(
        "teraBox",
        api_id=api_id, api_hash=api_hash,
        bot_token="1616731290:AAEbujGLXZkyV4iBGTfKypQ2s2sVWURvmj4"
    )

    try:
        await app.start()
        await asyncio.sleep(10)  # 2 minutes wait
    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
