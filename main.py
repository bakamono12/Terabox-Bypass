import time
import logging
from pyrogram import Client, filters, enums
from config import session_string, allowed_groups, owner_id
from downloader import check_url_patterns_async, fetch_download_link_async, get_formatted_size_async

app = Client("teraBox", session_string=session_string)
logging.basicConfig(level=logging.INFO)


@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await message.reply_text("⚠️ Forbidden!\nFor groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        await message.reply_text(
            "Hello! I'm Terabox link Bypass Bot. Send me a link to bypass.\n"
            "Owner: @DTMK_C\n"
            "Eg:- `https://teraboxapp.com/s/1Ykohv-bhT4SJJEgyDMeS-A`", quote=True)


@app.on_message(filters.command("ping"))
async def ping(client, message):
    if str(message.from_user.id) != owner_id:
        return
    start_time = time.time()
    await message.reply_text("Pong!")
    end_time = time.time()
    time_taken = end_time - start_time
    await message.reply_text(f"Pong!\nTime Taken: {time_taken:.2f} seconds")


async def format_message(link_data):
    file_name = link_data["server_filename"]
    file_size = await get_formatted_size_async(link_data["size"])
    download_link = link_data["dlink"]
    return f"┎ <b>Title</b>: `{file_name}`\n┠ <b>Size</b>: `{file_size}`\n┖ <b>Link</b>: <a href={download_link}>Link</a>"


@app.on_message(filters.regex(
    pattern=r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"))
async def link_handler(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await message.reply_text("⚠️ Forbidden! For groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        start_time = time.time()
        url = message.text
        if not await check_url_patterns_async(url):
            await message.reply_text("⚠️ Invalid URL!", quote=True)
            return
        try:
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
            await message.reply_text("🔎 Checking URL...", quote=True)
            link_data = await fetch_download_link_async(url)
            end_time = time.time()
            time_taken = end_time - start_time
            link_message = "\n\n".join([format_message(link) for link in link_data])
            download_message = (f"🔗 <b>Link Bypassed!</b>\n\n{link_message}\n\n<b>Time Taken</b>: {time_taken:.2f} "
                                f"seconds")
            await message.edit_text(download_message, quote=True)
        except Exception as e:
            await message.reply_text(f"Error: {e}", quote=True)


# run the application
app.run()
