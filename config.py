import os

headers_str = os.environ.get("MY_HEADERS")  # Replace "MY_HEADERS" with your actual environment variable name
my_headers = {}

if headers_str:
    header_pairs = headers_str.split("; ")
    for pair in header_pairs:
        name, value = pair.split(": ", 1)
        my_headers[name] = value

# Retrieve cookies from environment variable
cookies_str = os.environ.get("MY_COOKIES")  # Replace "MY_COOKIES" with your actual environment variable name
my_cookie = {}

if cookies_str:
    cookie_pairs = cookies_str.split("; ")
    for pair in cookie_pairs:
        name, value = pair.split("=", 1)
        my_cookie[name] = value

session_string = os.environ.get("session_string")
allowed_groups = os.environ.get("allowed_groups") or "-123232ZCVZB" # added random group id to avoid NoneType error
# allowed_groups = ["-123232ZCVZB"] or ["121222xxx", "123456xxx"]
owner_id = os.environ.get("owner_id") or ""