#!/usr/bin/env python3
"""
HTTP Status Codes - Show common HTTP status codes.
Usage: python http-status.py [code]
"""

import sys

STATUS_CODES = {
    100: ('Continue', 'The server has received the request headers'),
    101: ('Switching Protocols', 'The requester has asked the server to switch protocols'),
    200: ('OK', 'The request succeeded'),
    201: ('Created', 'The request succeeded and a new resource was created'),
    204: ('No Content', 'The request succeeded but returns no content'),
    301: ('Moved Permanently', 'The resource has been permanently moved'),
    302: ('Found', 'The resource has been temporarily moved'),
    304: ('Not Modified', 'The resource has not been modified'),
    400: ('Bad Request', 'The server cannot process the request'),
    401: ('Unauthorized', 'Authentication is required'),
    403: ('Forbidden', 'The server refuses to authorize the request'),
    404: ('Not Found', 'The resource cannot be found'),
    405: ('Method Not Allowed', 'The HTTP method is not allowed'),
    408: ('Request Timeout', 'The server timed out waiting for the request'),
    429: ('Too Many Requests', 'Rate limiting - try again later'),
    500: ('Internal Server Error', 'The server encountered an unexpected condition'),
    502: ('Bad Gateway', 'The server received an invalid response'),
    503: ('Service Unavailable', 'The server is temporarily unavailable'),
    504: ('Gateway Timeout', 'The server did not receive a timely response'),
}

CATEGORIES = {
    '1xx': 'Informational',
    '2xx': 'Success',
    '3xx': 'Redirection',
    '4xx': 'Client Error',
    '5xx': 'Server Error',
}

def print_category(cat):
    """Print status codes for a category."""
    print(f"=== {cat}xx {CATEGORIES[cat]} ===\n")
    for code, (name, desc) in STATUS_CODES.items():
        if str(code).startswith(cat[0]):
            print(f"{code} {name}")
            print(f"  {desc}")
            print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Print all
        for cat in ['1', '2', '3', '4', '5']:
            print_category(cat)
    else:
        code = int(sys.argv[1])
        if code in STATUS_CODES:
            name, desc = STATUS_CODES[code]
            cat = str(code)[0]
            print(f"{code} {name}")
            print(f"{CATEGORIES[cat + 'xx']}")
            print()
            print(desc)
        else:
            print(f"Unknown status code: {code}")
