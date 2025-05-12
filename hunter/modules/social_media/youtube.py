from hunter.core import *
from hunter.localuseragent import *

async def youtube(email, client, out):
    # Stub implementation
    out.append({
        "name": "youtube",
        "domain": "youtube.com",
        "rateLimit": False,
        "error": True,
        "exists": False,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    }) 