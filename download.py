import requests
import json


def downloader(share_id, uk, sign, timestamp, fs_id):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "140",
        "Content-Type": "application/json",
        "Dnt": "1",
        "Origin": "https://terabox-dl.qtcloud.workers.dev",
        "Pragma": "no-cache",
        "Referer": "https://terabox-dl.qtcloud.workers.dev/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    data = json.dumps(
        {"shareid": share_id, "uk": uk, "sign": str(sign),
         "timestamp": timestamp, "fs_id": str(fs_id)}
    )

    response = requests.post('https://terabox-dl.qtcloud.workers.dev/api/get-download', headers=headers, data=data)
    if response.status_code == 200 and response.json()['ok'] is True:
        return response.json()['downloadLink']
    else:
        return "Something went wrong try again after some time."


def fetch_details(url):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Dnt": "1",
        "Origin": "https://terabox-dl.qtcloud.workers.dev",
        "Pragma": "no-cache",
        "Referer": "https://terabox-dl.qtcloud.workers.dev/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    short_url = get_short_url(url)
    url = "https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl=1%s" % short_url
    response = requests.get(url=url, headers=headers, cert=False)
    if response.status_code == 200 and response.json()['ok'] is True:
        return response.json()
    else:
        return False


def get_short_url(url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }
    data = requests.get(url=url, headers=headers, allow_redirects=True, cert=False)
    if data.status_code == 200:
        return data.url.split("?surl=")[1]


def get_formatted_size(size_bytes):
    size, unit = None, None
    size_bytes = int(size_bytes)

    if size_bytes >= 1024 * 1024:
        size = size_bytes / (1024 * 1024)
        unit = "MB"
    elif size_bytes >= 1024:
        size = size_bytes / 1024
        unit = "KB"
    else:
        size = size_bytes
        unit = "bytes"

    return f"{size:.2f} {unit}"
