import os
import logging
logger = logging.getLogger(__name__)

my_cookie = os.environ.get("MY_COOKIES")
my_headers = os.environ.get("MY_HEADERS")
session_string = os.environ.get("session_string")
allowed_groups = os.environ.get("allowed_groups") or "-123232ZCVZB" # added random group id to avoid NoneType error
# allowed_groups = ["-123232ZCVZB"] or ["121222xxx", "123456xxx"]
owner_id = os.environ.get("owner_id") or ""

try:
    my_cookie = eval(my_cookie)
    my_headers = eval(my_headers)
    allowed_groups = eval(allowed_groups)
except Exception as e:
    logger.error(f"Error parsing env variables: {e}")
