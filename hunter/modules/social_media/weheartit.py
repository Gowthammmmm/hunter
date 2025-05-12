from hunter.core import *
from hunter.localuseragent import *

is_stub = True

async def weheartit(email, client, out):
    # Stub implementation
    out.append({
        "name": "weheartit",
        "domain": "weheartit.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 