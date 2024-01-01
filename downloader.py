import random
import re, os
from aria2p import API, Download, Client
import aiohttp
from config import my_cookie, my_headers
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

# set the environment vars for headers and cookies
my_session = aiohttp.ClientSession(cookies=my_cookie)
my_session.headers.update(my_headers)

domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN") or "http://localhost"
port = os.environ.get("PORT") or 6800


async def get_formatted_size_async(size_bytes):
    try:
        size_bytes = int(size_bytes)
        size = size_bytes / (1024 * 1024) if size_bytes >= 1024 * 1024 else (
            size_bytes / 1024 if size_bytes >= 1024 else size_bytes
        )
        unit = "MB" if size_bytes >= 1024 * 1024 else ("KB" if size_bytes >= 1024 else "bytes")

        return f"{size:.2f} {unit}"
    except Exception as e:
        print(f"Error getting formatted size: {e}")
        return None


async def is_valid_url_async(url):
    try:
        async with my_session.get(url) as response:
            return response.status == 200
    except Exception as e:
        return False


async def check_url_patterns_async(url):
    patterns = [
        r"ww\.mirrobox\.com",
        r"www\.nephobox\.com",
        r"freeterabox\.com",
        r"www\.freeterabox\.com",
        r"1024tera\.com",
        r"4funbox\.co",
        r"www\.4funbox\.com",
        r"mirrobox\.com",
        r"nephobox\.com",
        r"terabox\.app",
        r"terabox\.com",
        r"www\.terabox\.ap",
        r"terabox\.fun",
        r"www\.terabox\.com",
        r"www\.1024tera\.co",
        r"www\.momerybox\.com",
        r"teraboxapp\.com",
        r"momerybox\.com",
        r"tibibox\.com",
        r"www\.tibibox\.com",
        r"www\.teraboxapp\.com",
    ]

    if not await is_valid_url_async(url):
        return False

    for pattern in patterns:
        if re.search(pattern, url):
            return True
    return False


async def find_between(string, start, end):
    start_index = string.find(start) + len(start)
    end_index = string.find(end, start_index)
    return string[start_index:end_index]


async def fetch_download_link_async(url):
    try:
        async with my_session.get(url) as response:
            response.raise_for_status()
            response_data = await response.text()

            js_token = await find_between(response_data, 'fn%28%22', '%22%29')
            log_id = await find_between(response_data, 'dp-logid=', '&')

            if not js_token or not log_id:
                return None

            request_url = str(response.url)
            surl = request_url.split('surl=')[1]
            params = {
                'app_id': '250528',
                'web': '1',
                'channel': 'dubox',
                'clienttype': '0',
                'jsToken': js_token,
                'dplogid': log_id,
                'page': '1',
                'num': '20',
                'order': 'time',
                'desc': '1',
                'site_referer': request_url,
                'shorturl': surl,
                'root': '1'
            }
            random_url = random.choice(["https://www.1024tera.com/share/list", "https://www.terabox.app/share/list",
                                        "https://www.4funbox.com/share/list"])
            async with my_session.get(random_url, params=params) as response2:
                response_data2 = await response2.json()
                if 'list' not in response_data2:
                    return None
                return response_data2['list']
    except aiohttp.ClientResponseError as e:
        logger.error(f"Error fetching download link: {e}")
        return None


async def fetch_final_link_async(url):
    try:
        async with my_session.get(url, allow_redirects=True) as response:
            response.raise_for_status()
            return str(response.url)
    except aiohttp.ClientResponseError as e:
        logging.error(f"Error fetching download link: {e}")
        print(f"Error fetching download link: {e}")
        return None


class Aria2Downloader:
    def __init__(self, download_dir='downloads'):
        self.download_dir = download_dir
        self.aria2 = API(Client(
            host=domain,
            port=port,
            secret="baka")
        )

    def start_download(self, url: list):
        options = {
            'dir': self.download_dir,
        }
        download = self.aria2.add_uris(url, options=options)
        # threading.Thread(target=self._check_download_status(download), args=(download,), daemon=True).start()
        return self._check_download_status(download)

    def _check_download_status(self, download: Download):
        while not download.is_complete:
            download.update()
            status = download.status
            download_speed = download.download_speed_string or 0
            eta = download.eta_string or 0

            progress_info = {
                'gid': download.gid,
                'status': status,
                'name': download.name,
                'downloaded': download.progress_string(),
                'download_speed': download_speed(),
                'eta': eta(),
                'is_complete': download.is_complete
            }
            yield progress_info
        return f"Download complete: {download.name} ({download.files[0]})"

    def cancel_download(self, gid):
        download = self.aria2.get_download(gid)
        if download:
            download.remove()

    def pause_download(self, gid):
        download = self.aria2.get_download(gid)
        if download:
            download.pause()

    def resume_download(self, gid):
        download = self.aria2.get_download(gid)
        if download:
            download.resume()
