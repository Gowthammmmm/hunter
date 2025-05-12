from hunter.core import *
from hunter.localuseragent import *

is_stub = True

async def spotify(email, client, out):
    # Stub implementation
    out.append({
        "name": "spotify",
        "domain": "spotify.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 