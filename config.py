import os
import logging
import re
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

MY_COOKIES = os.environ.get("MY_COOKIES")
MY_HEADERS = os.environ.get("MY_HEADERS")
SESSION_STRING = os.environ.get("SESSION_STRING")
ALLOWED_GROUPS = os.environ.get("ALLOWED_GROUPS") or "-123232ZCVZB"  # added random group id to avoid NoneType error
# ALLOWED_GROUPS = ["-123232ZCVZB"] or ["121222xxx", "123456xxx"]
OWNER_ID = os.environ.get("OWNER_ID") or ""

try:
    MY_COOKIES = eval(MY_COOKIES)
    MY_HEADERS = eval(MY_HEADERS)
    ALLOWED_GROUPS = eval(ALLOWED_GROUPS)
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
