from hunter.core import *
from hunter.localuseragent import *

is_stub = True

async def tiktok(email, client, out):
    # Stub implementation
    out.append({
        "name": "tiktok",
        "domain": "tiktok.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 