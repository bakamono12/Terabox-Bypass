import asyncio
import os
import random
import time
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import session_string, allowed_groups, owner_id, extract_links, extract_gid, EMOJI, PATH
from downloader import check_url_patterns_async, fetch_download_link_async, get_formatted_size_async, Aria2Downloader

app = Client("teraBox", session_string=session_string)
logger = logging.getLogger(__name__)

# initialize downloader
downloader = Aria2Downloader()

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
            buttons = [
                InlineKeyboardButton("Download", callback_data="download"),
            ]
            for url in urls:
                if not await check_url_patterns_async(url):
                    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                    await message.reply_text("⚠️ No valid Terabox URLs Found!", quote=True)
                    continue
                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                process_url = await message.reply_text("🔎 Processing URL...", quote=True)
                end_time = time.time()
                link_data = await fetch_download_link_async(url)
                time_taken = end_time - start_time
                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                link_message = "\n\n".join([await format_message(link) for link in link_data])
                download_message = (
                    f"🔗 <b>Link Bypassed!</b>\n\n{link_message}\n\n<b>Time Taken</b>: {time_taken:.2f} seconds"
                )
                await process_url.edit_text(download_message, reply_markup=InlineKeyboardMarkup([buttons]),
                                            disable_web_page_preview=True)

        except Exception as e:
            await message.reply_text(f"Error: {e}", quote=True)


@app.on_callback_query(filters.regex(r"download"))
async def download_handler(client, callback_data):
    url = callback_data.message.reply_to_message.text
    # check if the link sender and the button clicker are the same
    if callback_data.from_user.id != callback_data.message.reply_to_message.from_user.id:
        await callback_data.answer("You didn't send this link.", show_alert=True)
        return
    cancel_buttons = [
        InlineKeyboardButton("Cancel", callback_data="cancel"),
    ]
    # Initialize the download
    files = downloader.start_download(url)
    response_text = "Starting download..."
    for file_update in files:
        try:
            response_text = (
                f"Status: `{file_update['status']}`\n"
                f"Name: `{file_update['name']}`\n"
                f"Downloaded: `{file_update['downloaded']}`\n"
                f"Speed: `{file_update['download_speed']}`\n"
                f"ETA: `{file_update['eta']}`\n"
                f"GID: `{file_update['gid']}`"
            )
            await callback_data.edit_message_text(response_text, reply_markup=InlineKeyboardMarkup([cancel_buttons]))
            if file_update['is_complete']:
                response_text = (
                    f"Status: `{file_update['status']}`\n"
                    f"Name: `{file_update['name']}`\n"
                    f"Downloaded: `{file_update['downloaded']}\n`"
                    f"GID: `{file_update['gid']}`"
                )
                await callback_data.edit_message_text(response_text)
                break
            await asyncio.sleep(3.5)
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(2.5)
            await callback_data.edit_message_text(f"Some Error Occurred: {e}\n\n {random.choice(EMOJI)}")


@app.on_callback_query(filters.regex(r"cancel"))
async def cancel_download_handler(client, callback_data):
    # Handle cancel button click
    name, gid = await extract_gid(callback_data.message.text)
    if gid:
        try:
            downloader.cancel_download(gid)
            os.remove(PATH + "/" + name)
            await callback_data.message.edit_text("Download cancelled and removed.")
            return
        except Exception as e:
            logger.error(e)
            await callback_data.message.edit_text(f"Some Error Occurred: {e}\n\n {random.choice(EMOJI)}")
            return
    await callback_data.message.edit_text("Download already completed/Cancelled/Removed.")


# run the application
app.run()
