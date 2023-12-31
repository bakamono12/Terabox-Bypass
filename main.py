import time
import logging
from pyrogram import Client, filters, enums
from config import session_string, allowed_groups, owner_id, extract_links
from downloader import check_url_patterns_async, fetch_download_link_async, get_formatted_size_async

app = Client("teraBox", session_string=session_string)
logging.basicConfig(level=logging.INFO)


@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden!\nFor groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text(
            "Hello! I'm Terabox link Bypass Bot. Send me a link to bypass.\n"
            "Owner: @DTMK_C\n"
            "Eg:- `https://teraboxapp.com/s/1Ykohv-bhT4SJJEgyDMeS-A`", quote=True)


@app.on_message(filters.command("ping"))
async def ping(client, message):
    if str(message.from_user.id) != owner_id:
        return
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    start_time = time.time()
    sent_message = await message.reply_text("Pong!", quote=True)
    end_time = time.time()
    time_taken = end_time - start_time
    await sent_message.edit_text(f"Pong!\nTime Taken: {time_taken:.2f} seconds")


async def format_message(link_data):
    file_name = link_data["server_filename"]
    file_size = await get_formatted_size_async(link_data["size"])
    download_link = link_data["dlink"]
    return f"┎ <b>Title</b>: `{file_name}`\n┠ <b>Size</b>: `{file_size}`\n┖ <b>Link</b>: <a href={download_link}>Link</a>"


@app.on_message(filters.regex(
    pattern=r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"))
async def link_handler(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden! For groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        start_time = time.time()
        urls = extract_links(message.text) + extract_links(message.caption)
        if not urls:
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
            await message.reply_text("⚠️ No valid URLs found!", quote=True)
            return
        try:
            for url in urls:
                if not await check_url_patterns_async(url):
                    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                    await message.reply_text("⚠️ Not a valid Terabox URL!", quote=True)
                    continue

                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                process_url = await message.reply_text("🔎 Processing URL...", quote=True)
                link_data = await fetch_download_link_async(url)

                end_time = time.time()
                time_taken = end_time - start_time
                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

                link_message = "\n\n".join([await format_message(link) for link in link_data])
                download_message = (
                    f"🔗 <b>Link Bypassed!</b>\n\n{link_message}\n\n<b>Time Taken</b>: {time_taken:.2f} seconds"
                )
                await process_url.edit_text(download_message)

        except Exception as e:
            await message.reply_text(f"Error: {e}", quote=True)


# run the application
app.run()
