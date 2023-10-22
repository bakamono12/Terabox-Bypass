from download import fetch_details, downloader, get_formatted_size
from pyrogram import Client, filters

app = Client("teraBox")


@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(
        "Hello! I'm Terabox link Bypass Bot. Send me a link to download from Terabox.\nFor bypassing a link "
        "use\n/bypass `https://teraboxapp.com/s/1Ykohv-bhT4SJJEgyDMeS-A`", quote=True)


@app.on_message(filters.command("bypass"))
def bypass(client, message):
    try:
        url = message.text.split(" ", 1)[1]
        files = fetch_details(url)
        if files:
            video_links = list()
            data = files
            for item in data['list']:
                if item['is_dir'] == '0':
                    fs_id = item['fs_id']
                    timestamp = data['timestamp']
                    sign = data['sign']
                    share_id = data['shareid']
                    uk = data['uk']
                    download_link = downloader(share_id, uk, sign, timestamp, fs_id)
                    video_links.append(
                        {'name': item['filename'], 'size': get_formatted_size(item['size']), 'link': download_link})
                elif item['is_dir'] == '1':
                    for child_item in item['children']:
                        fs_id = child_item['fs_id']
                        timestamp = data['timestamp']
                        sign = data['sign']
                        share_id = data['shareid']
                        uk = data['uk']
                        download_link = downloader(fs_id, timestamp, sign, share_id, uk)
                        video_links.append(
                            {'name': child_item['filename'], 'size': get_formatted_size(child_item['size']),
                             'link': download_link})
            # format the links to send
            text = ""
            for link in video_links:
                text += f"Name 📹 : {link['name']}\n\nSize 📏 : {link['size']}\n\nDLink 📥 : [Click here]({link['link']})\n\n"
            text += "\nCreated By [Ⴆαƙα](t.me/DTMK_C)"
            message.reply_text(text, quote=True, disable_web_page_preview=True)
        else:
            message.reply_text("Invalid URL", quote=True)
    except IndexError as e:
        message.reply_text("Enter the URL", quote=True)

# run the application
app.run()
