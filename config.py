import os
import logging
import re

logger = logging.getLogger(__name__)
my_cookie = os.environ.get("MY_COOKIES")
my_headers = os.environ.get("MY_HEADERS")
session_string = os.environ.get("session_string")
allowed_groups = os.environ.get("allowed_groups") or "-123232ZCVZB"  # added random group id to avoid NoneType error
# allowed_groups = ["-123232ZCVZB"] or ["121222xxx", "123456xxx"]
owner_id = os.environ.get("owner_id") or ""
PATH = "./downloads"
EMOJI = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘",
         "😗", "😙", "😚", ]

try:
    my_cookie = eval(my_cookie)
    my_headers = eval(my_headers)
    allowed_groups = eval(allowed_groups)
except Exception as e:
    logger.error(f"Error parsing env variables: {e}")


def extract_links(message):
    # fetch all links
    try:
        url_pattern = r'https?://\S+'
        matches = re.findall(url_pattern, message)
        return matches
    except Exception as e:
        logger.error(f"Error extracting links: {e}")
        return []


async def extract_gid(message_update):
    gid = [item.split(':')[1].strip() for item in message_update.split('\n') if 'GID' in item or 'Name' in item]
    return gid if gid else None
